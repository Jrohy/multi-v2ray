#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import random
import string
import uuid

from .config import Config
from .utils import port_is_use, StreamType, random_port
from .loader import Loader
from .group import Mtproto, Vmess, Socks

def clean_mtproto_tag(config, group_index):
    '''
    清理mtproto 协议减少时无用的tag
    '''
    if "tag" in config["inbounds"][group_index]:
        tag = config["inbounds"][group_index]["tag"]

        rules = config["routing"]["rules"]

        for index, rule in enumerate(rules):
            if rule["outboundTag"] != "tg-out":
                continue
            if len(rule["inboundTag"]) == 1:
                del rules[index]
                for out_index, oubound_mtproto in enumerate(config["outbounds"]):
                    if oubound_mtproto["protocol"] == "mtproto":
                        del config["outbounds"][out_index]
                        break
            else:
                for tag_index, rule_tag in enumerate(rule["inboundTag"]):
                    if rule_tag == tag:
                        del rule["inboundTag"][tag_index]
                        break
            break

class Writer:
    def __init__(self, group_tag = 'A', group_index=0):
        self.multi_config = Config()
        self.group_index = group_index
        self.group_tag = group_tag
        self.path = self.multi_config.get_path('config_path')
        self.template_path = self.multi_config.json_path
        self.config = self.load(self.path)
        self.part_json = self.config["inbounds"][self.group_index]

    def load(self, path):
        '''
        load v2ray profile
        '''
        with open(path, 'r') as json_file:
            config = json.load(json_file)
        return config

    def load_template(self, template_name):
        '''
        load special template
        '''
        with open(self.template_path + "/" + template_name, 'r') as stream_file:
            template = json.load(stream_file)
        return template

    def save(self):
        '''
        save v2ray config.json
        '''
        json_dump=json.dumps(self.config, indent=2)
        with open(self.path, 'w') as writer:
            writer.writelines(json_dump)

class StreamWriter(Writer):
    def __init__(self, group_tag, group_index, stream_type=None):
        super(StreamWriter, self).__init__(group_tag, group_index)
        self.stream_type = stream_type
    
    def to_mtproto(self, template_json):
        mtproto_in = template_json["mtproto-in"]
        mtproto_in["port"] = self.part_json["port"]
        mtproto_in["tag"] = self.group_tag
        if "allocate" in self.part_json:
            mtproto_in["allocate"] = self.part_json["allocate"]
        salt = "abcdef" + string.digits
        secret = ''.join([random.choice(salt) for _ in range(32)])
        mtproto_in["settings"]["users"][0]["secret"] = secret
        self.part_json = mtproto_in

        has_outbound = False
        for outbound in self.config["outbounds"]:
            if "protocol" in outbound and outbound["protocol"] == "mtproto":
                has_outbound = True
                break
        if not has_outbound:
            mtproto_out = template_json["mtproto-out"]
            self.config["outbounds"].append(mtproto_out)
        
        rules = self.config["routing"]["rules"]
        has_bind = False
        for rule in rules:
            if rule["outboundTag"] == "tg-out":
                has_bind = True
                inbound_tag_set = set(rule["inboundTag"])
                inbound_tag_set.add(self.group_tag)
                rule["inboundTag"] = list(inbound_tag_set)
                break
        if not has_bind:
            routing_bind = template_json["routing-bind"]
            routing_bind["inboundTag"][0] = self.group_tag
            rules.append(routing_bind)

    def write(self, **kw):
        security_backup, tls_settings_backup, origin_protocol = "", "", None

        if self.part_json['protocol'] == 'shadowsocks':
            origin_protocol = StreamType.SS
        elif self.part_json['protocol'] == 'mtproto':
            origin_protocol = StreamType.MTPROTO
        elif self.part_json['protocol'] == 'socks':
            origin_protocol = StreamType.SOCKS

        if origin_protocol != StreamType.MTPROTO and origin_protocol != StreamType.SS:
            security_backup = self.part_json["streamSettings"]["security"]
            tls_settings_backup = self.part_json["streamSettings"]["tlsSettings"]

        #mtproto换成其他协议时, 减少mtproto int和out的路由绑定
        if origin_protocol == StreamType.MTPROTO and origin_protocol != self.stream_type:
            clean_mtproto_tag(self.config, self.group_index)

        #原来是socks/mtproto/shadowsocks协议 则先切换为标准的inbound
        if origin_protocol == StreamType.MTPROTO or origin_protocol == StreamType.SOCKS or origin_protocol == StreamType.SS:
            vmess = self.load_template('server.json')
            vmess["inbounds"][0]["port"] = self.part_json["port"]
            if "allocate" in self.part_json:
                vmess["inbounds"][0]["allocate"] = self.part_json["allocate"]
            self.part_json = vmess["inbounds"][0]

        if self.stream_type == StreamType.KCP:
            self.part_json["streamSettings"] = self.load_template('kcp.json')
        
        elif self.stream_type == StreamType.KCP_UTP:
            self.part_json["streamSettings"] = self.load_template('kcp.json')
            self.part_json["streamSettings"]["kcpSettings"]["header"]["type"] = "utp"

        elif self.stream_type == StreamType.KCP_SRTP:
            self.part_json["streamSettings"] = self.load_template('kcp.json')
            self.part_json["streamSettings"]["kcpSettings"]["header"]["type"] = "srtp"

        elif self.stream_type == StreamType.KCP_WECHAT:
            self.part_json["streamSettings"] = self.load_template('kcp.json')
            self.part_json["streamSettings"]["kcpSettings"]["header"]["type"] = "wechat-video"

        elif self.stream_type == StreamType.KCP_DTLS:
            self.part_json["streamSettings"] = self.load_template('kcp.json')
            self.part_json["streamSettings"]["kcpSettings"]["header"]["type"] = "dtls"

        elif self.stream_type == StreamType.KCP_WG:
            self.part_json["streamSettings"] = self.load_template('kcp.json')
            self.part_json["streamSettings"]["kcpSettings"]["header"]["type"] = "wireguard"

        elif self.stream_type == StreamType.TCP:
            self.part_json["streamSettings"] = self.load_template('tcp.json')

        elif self.stream_type == StreamType.TCP_HOST:
            http = self.load_template('http.json')
            http["tcpSettings"]["header"]["request"]["headers"]["Host"] = kw["host"]
            self.part_json["streamSettings"] = http

        elif self.stream_type == StreamType.MTPROTO:
            mtproto = self.load_template('mtproto.json')
            self.to_mtproto(mtproto)

        elif self.stream_type == StreamType.QUIC:
            quic = self.load_template('quic.json')
            quic["quicSettings"]["security"] = kw["security"]
            quic["quicSettings"]["key"] = kw["key"]
            quic["quicSettings"]["header"]["type"] = kw["header"]
            self.part_json["streamSettings"] = quic

        elif self.stream_type == StreamType.SOCKS:
            socks = self.load_template('socks.json')
            tcp = self.load_template('tcp.json')
            socks["accounts"][0]["user"] = kw["user"]
            socks["accounts"][0]["pass"] = kw["pass"]
            self.part_json["settings"] = socks
            self.part_json["protocol"] = "socks"
            self.part_json["streamSettings"] = tcp

        elif self.stream_type == StreamType.SS:
            ss = self.load_template('ss.json')
            ss["port"] = self.part_json["port"]
            if "allocate" in self.part_json:
                ss["allocate"] = self.part_json["allocate"]
            ss["settings"]["method"] = kw["method"]
            ss["settings"]["password"] = kw["password"]
            self.part_json = ss
        
        elif self.stream_type == StreamType.WS:
            ws = self.load_template('ws.json')
            salt = '/' + ''.join(random.sample(string.ascii_letters + string.digits, 8)) + '/'
            ws["wsSettings"]["path"] = salt
            if "host" in kw:
                ws["wsSettings"]["headers"]["Host"] = kw['host']
            self.part_json["streamSettings"] = ws

        elif self.stream_type == StreamType.H2:
            http2 = self.load_template('http2.json')
            salt = '/' + ''.join(random.sample(string.ascii_letters + string.digits, 8)) + '/'
            http2["httpSettings"]["path"] = salt
            self.config["inbounds"][self.group_index]["streamSettings"] = http2
            self.save()

            # http2 tls的设置
            if security_backup != "tls" or not "certificates" in tls_settings_backup:
                from ..config_modify.tls import TLSModifier
                tm = TLSModifier(self.group_tag, self.group_index)
                tm.turn_on()
                return

        if (self.stream_type != StreamType.MTPROTO and origin_protocol != StreamType.MTPROTO 
           and self.stream_type != StreamType.SS and origin_protocol != StreamType.SS):
            self.part_json["streamSettings"]["security"] = security_backup
            self.part_json["streamSettings"]["tlsSettings"] = tls_settings_backup

        self.config["inbounds"][self.group_index] = self.part_json
        self.save()

class GroupWriter(Writer):
    def __init__(self, group_tag, group_index):
        super(GroupWriter, self).__init__(group_tag, group_index)

    def write_port(self, port):
        self.part_json["port"] = str(port) if str(port).find("-") > 0 else int(port)
        self.save()

    def write_domain(self, domain=''):
        if domain:
            self.part_json["domain"] = domain
        elif "domain" in self.part_json:
            del self.part_json["domain"]
        self.save()

    def write_ss_password(self, new_password):
        self.part_json["settings"]["password"] = str(new_password)
        self.save()

    def write_ss_method(self, new_method):
        self.part_json["settings"]["method"] = str(new_method)
        self.save()

    def write_ss_email(self, email):
        if "email" in self.part_json["settings"]:
            self.part_json["settings"].update({"email": email})
        else:
            self.part_json["settings"]["email"] = email
        self.save()

    def write_dyp(self, status = False, aid = '32'):
        if status:
            short_uuid = str(uuid.uuid1())[0:7]
            dynamic_port_tag = "dynamicPort" + short_uuid
            self.part_json["settings"].update({"detour":{"to":dynamic_port_tag}})
            dyn_json = self.load_template('dyn_port.json')
            dyn_json["settings"]["default"]["alterId"] = int(aid)
            dyn_json["tag"] = dynamic_port_tag
            self.config["inbounds"].append(dyn_json)
        else:
            dynamic_port_tag = self.part_json["settings"]["detour"]["to"]
            for index, inbound in enumerate(self.config["inbounds"]):
                if "tag" in inbound and inbound["tag"] == dynamic_port_tag:
                    del self.config["inbounds"][index]
                    break
            if "detour" in self.part_json["settings"]:
                del self.part_json["settings"]["detour"]
        self.save()

    def write_tls(self, status = False, *, crt_file=None, key_file=None, domain=None):
        if status:
            tls_settings = {"certificates": [
                {
                "certificateFile": crt_file,
                "keyFile": key_file
                }
            ]}
            self.part_json["streamSettings"]["security"] = "tls"
            self.part_json["streamSettings"]["tlsSettings"] = tls_settings
            self.part_json["domain"] = domain
            self.save()
        else:
            if self.part_json["streamSettings"]["network"] == StreamType.H2.value:
                print(_("close tls will also close HTTP/2!"))
                print("")
                print(_("already reset protocol to origin kcp"))
                self.part_json["streamSettings"] = self.load_template('kcp.json')
            else:
                self.part_json["streamSettings"]["security"] = "none"
                self.part_json["streamSettings"]["tlsSettings"] = {}
            self.save()

    def write_tfo(self, action = 'del'):
        if action == "del":
            if "sockopt" in self.part_json["streamSettings"]:
                del self.part_json["streamSettings"]["sockopt"]
        else:
            sockoptDict = {"mark":0, "tcpFastOpen": False}
            if action == "on":
                sockoptDict['tcpFastOpen'] = True
            if "sockopt" in self.part_json["streamSettings"]:
                self.part_json["streamSettings"]["sockopt"] = sockoptDict
            else:
                self.part_json["streamSettings"].update({"sockopt":sockoptDict})
        self.save()

class ClientWriter(Writer):
    def __init__(self, group_tag = 'A', group_index = 0, client_index = 0):
        super(ClientWriter, self).__init__(group_tag, group_index)
        self.client_index = client_index
        self.client_str = "clients" if self.part_json["protocol"] == "vmess" else "users"

    def write_aid(self, aid = 32):
        self.part_json["settings"][self.client_str][self.client_index]["alterId"] = int(aid)
        self.save()

    def write_uuid(self, new_uuid):
        self.part_json["settings"][self.client_str][self.client_index]["id"] = str(new_uuid)
        self.save()

    def write_email(self, email):
        if self.part_json["protocol"] == "shadowsocks":
            self.part_json["settings"].update({"email": email})
        else:
            self.part_json["settings"][self.client_str][self.client_index].update({"email": email})
        self.save()

class GlobalWriter(Writer):

    def __init__(self, group_list):
        super(GlobalWriter, self).__init__()
        self.group_list = group_list

    def write_ban_bittorrent(self, status = False):
        '''
        禁止BT设置
        '''
        conf_rules = self.config["routing"]["rules"]
        if status:
            for group in self.group_list:
                if "sniffing" not in self.config["inbounds"][group.index]:
                    self.config["inbounds"][group.index].update({
                        "sniffing": {
                            "enabled": True,
                            "destOverride": ["http", "tls"]
                        }
                    })
            has_rule = False
            for rule in conf_rules:
                if "protocol" in rule and "bittorrent" in rule["protocol"]:
                    has_rule = True
                    break
            if not has_rule:
                self.config["routing"]["rules"].append(
                    {
                        "type": "field",
                        "outboundTag": "blocked",
                        "protocol": [
                            "bittorrent"
                        ]
                    }
                )
        else:
            for group in self.group_list:
                if "sniffing" in self.config["inbounds"][group.index]:
                    del self.config["inbounds"][group.index]["sniffing"]

            for index, rule in enumerate(conf_rules):
                if "protocol" in rule and "bittorrent" in rule["protocol"]:
                    del self.config["routing"]["rules"][index]

        self.save()

    def write_stats(self, status = False):
        '''
        更改流量统计设置
        '''
        conf_rules = self.config["routing"]["rules"]
        if status:
            stats_json = self.load_template('stats_settings.json')
            routing_rules = stats_json["routingRules"]
            del stats_json["routingRules"]

            has_rule = False
            for rule in conf_rules:
                if rule["outboundTag"] == "api":
                    has_rule = True
                    break
            if not has_rule:
                conf_rules.append(routing_rules)

            dokodemo_door = stats_json["dokodemoDoor"]
            del stats_json["dokodemoDoor"]
            #产生随机dokodemo_door的连接端口
            dokodemo_door["port"] = random_port(1000, 65535)

            has_door = False
            for inbound in self.config["inbounds"]:
                if inbound["protocol"] == "dokodemo-door" and inbound["tag"] == "api":
                    has_door = True 
                    break
            if not has_door:
                self.config["inbounds"].append(dokodemo_door)

            #加入流量统计三件套
            self.config.update(stats_json)

            # 为各个组节点打上tag, 以便流量统计
            for group in self.group_list:
                if type(group) == Mtproto:
                    continue
                self.config["inbounds"][group.index].update({"tag": group.tag})
        else:
            # 删除用于统计流量的tag标签
            for index, inbound in enumerate(self.config["inbounds"]):
                if inbound["protocol"] == "dokodemo-door" and inbound["tag"] == "api":
                    del self.config["inbounds"][index]
                elif "tag" in inbound:
                    del self.config["inbounds"][index]["tag"]

            if "stats" in self.config:
                del self.config["stats"]
            if "api" in self.config:
                del self.config["api"]
            if "policy" in self.config:
                del self.config["policy"]

            for index, rule in enumerate(conf_rules):
                if rule["outboundTag"] == "api":
                    del conf_rules[index]
        self.save()

class NodeWriter(Writer):
    def create_new_port(self, newPort, protocol, **kw):
        # init new inbound
        server = self.load_template('server.json')
        new_inbound = server["inbounds"][0]
        new_inbound["port"] = int(newPort)
        new_inbound["settings"]["clients"][0]["id"] = str(uuid.uuid1())
        self.config["inbounds"].append(new_inbound)
        print(_("add port group success!"))
        self.save()

        reload_data = Loader()
        new_group_list = reload_data.profile.group_list
        stream_writer = StreamWriter(new_group_list[-1].tag, new_group_list[-1].index, protocol)
        stream_writer.write(**kw)

    def create_new_user(self, **kw):
        '''
        初始化时需传入group_tag, group_index参数, 自动调用父构造器来初始化
        '''
        if self.part_json['protocol'] == 'socks':
            user = {"user": kw["user"], "pass": kw["pass"]}
            self.part_json["settings"]["accounts"].append(user)
            print("{0} user: {1}, pass: {2}".format(_("add socks5 user success!"), kw["user"], kw["pass"]))
        
        elif self.part_json['protocol'] == 'vmess' :
            new_uuid = uuid.uuid1()
            email_info = ""
            user = {
                "alterId": 32,
                "id": "ae1bc6ce-e575-4ee2-85f1-350a0aa506cb"
            }
            if "email" in kw and kw["email"] != "":
                user.update({"email":kw["email"]})
                email_info = ", email: " + kw["email"]
            user["id"]=str(new_uuid)
            self.part_json["settings"]["clients"].append(user)
            print("{0} uuid: {1}, alterId: 32{2}".format(_("add user success!"), str(new_uuid), email_info))

        self.save()

    def del_user(self, group, client_index):
        node = group.node_list[0]
        if len(group.node_list) == 1:
            if type(node) == Mtproto:
                clean_mtproto_tag(self.config, group.index)
            del self.config["inbounds"][group.index]
        elif type(node) == Vmess or type(node) == Socks:
            client_str = 'clients' if type(node) == Vmess else 'accounts'
            del self.config["inbounds"][group.index]["settings"][client_str][client_index]

        print(_("del user success!"))
        self.save()

    def del_port(self, group):
        if type(group.node_list[0]) == Mtproto:
            clean_mtproto_tag(self.config, group.index)
        del self.config["inbounds"][group.index]
        print(_("del port success!"))
        self.save()