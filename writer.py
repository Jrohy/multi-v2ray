#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import random
import string
import uuid
from enum import Enum, unique

from utils import port_is_use
from loader import Loader
from group import Mtproto, Vmess, Socks

def clean_mtproto_tag(config, group_index):
    '''
    清理mtproto 协议减少时无用的tag
    '''
    rules = config["routing"]["settings"]["rules"]

    if group_index == -1:
        tag = config["inbound"]["tag"]
    else:
        tag = config["inboundDetour"][group_index]["tag"]

    for index, rule in enumerate(rules):
        if rule["outboundTag"] != "tg-out":
            continue
        if len(rule["inboundTag"]) == 1:
            del rules[index]
            for out_index, oubound_mtproto in enumerate(config["outboundDetour"]):
                if oubound_mtproto["protocol"] == "mtproto":
                    del config["outboundDetour"][out_index]
                    break
        else:
            for tag_index, rule_tag in enumerate(rule["inboundTag"]):
                if rule_tag == tag:
                    del rule["inboundTag"][tag_index]
                    break
        break

def stream_list():
    return [
        ("wireguard", StreamType.KCP_WG), 
        ("dtls", StreamType.KCP_DTLS), 
        ("wechat", StreamType.KCP_WECHAT), 
        ("utp", StreamType.KCP_UTP), 
        ("srtp", StreamType.KCP_SRTP), 
        ("mtproto", StreamType.MTPROTO), 
        ("socks", StreamType.SOCKS),
        ("ss", StreamType.SS)
    ]

@unique
class StreamType(Enum):
    TCP = 'tcp'
    TCP_HOST = 'tcp_host'
    SOCKS = 'socks'
    SS = 'shadowsocks'
    MTPROTO = 'mtproto'
    H2 = 'h2'
    WS = 'ws'
    KCP = 'kcp'
    KCP_UTP = 'kcp_utp'
    KCP_SRTP = 'kcp_srtp'
    KCP_DTLS = 'kcp_dtls'
    KCP_WECHAT = 'kcp_wechat'
    KCP_WG = 'kcp_wg'

class Writer:
    def __init__(self, group_tag='A', group_index=-1, path='/etc/v2ray/config.json', template_path='/usr/local/multi-v2ray/json_template'):
        self.group_tag = group_tag
        self.group_index = group_index
        self.path = path
        self.template_path = template_path
        self.config = self.load(path)
        self.part_json = None

    def load(self, path):
        '''
        load v2ray profile
        '''
        #打开配置文件
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
        if self.part_json:
            if self.group_tag == 'A':
                self.config["inbound"] = self.part_json
            else:
                self.config["inboundDetour"][self.group_index] = self.part_json

        json_dump=json.dumps(self.config, indent=1)
        with open(self.path, 'w') as writer:
            writer.writelines(json_dump)

    def locate_json(self):
        '''
        inbound级别定位json
        '''
        if self.group_tag == 'A':
            self.part_json = self.config["inbound"]
        else:
            self.part_json = self.config["inboundDetour"][self.group_index]

class StreamWriter(Writer):
    def __init__(self, group_tag, group_index, stream_type=None):
        super(StreamWriter, self).__init__(group_tag, group_index)
        self.stream_type = stream_type
        self.locate_json()
    
    def to_mtproto(self, template_json):
        mtproto_in = template_json["mtproto-in"]
        mtproto_in["port"] = self.part_json["port"]
        mtproto_in["tag"] = self.group_tag
        salt = "abcdef" + string.digits
        secret = ''.join([random.choice(salt) for _ in range(32)])
        mtproto_in["settings"]["users"][0]["secret"] = secret
        self.part_json = mtproto_in

        has_outbound = False
        for outbound in self.config["outboundDetour"]:
            if "protocol" in outbound and outbound["protocol"] == "mtproto":
                has_outbound = True
                break
        if not has_outbound:
            mtproto_out = template_json["mtproto-out"]
            self.config["outboundDetour"].append(mtproto_out)
        
        rules = self.config["routing"]["settings"]["rules"]
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

        for menber in StreamType.__members__.items():
            if menber[1].value == self.part_json['protocol']:
                origin_protocol = menber[1]
                break

        if origin_protocol != StreamType.MTPROTO and origin_protocol != StreamType.SS:
            security_backup = self.part_json["streamSettings"]["security"]
            tls_settings_backup = self.part_json["streamSettings"]["tlsSettings"]

        #mtproto换成其他协议时, 减少mtproto int和out的路由绑定
        if origin_protocol == StreamType.MTPROTO and origin_protocol != self.stream_type:
            clean_mtproto_tag(self.config, self.group_index)
            self.locate_json()

        #原来是socks/mtproto/shadowsocks协议 则先切换为标准的inbound
        if origin_protocol == StreamType.MTPROTO or origin_protocol == StreamType.SOCKS or origin_protocol == StreamType.SS:
            vmess = self.load_template('server.json')
            vmess["inbound"]["port"] = self.part_json["port"]
            self.part_json = vmess["inbound"]

        if self.stream_type == StreamType.KCP:
            self.part_json["streamSettings"] = self.load_template('kcp.json')
        
        elif self.stream_type == StreamType.KCP_UTP:
            self.part_json["streamSettings"] = self.load_template('kcp_utp.json')

        elif self.stream_type == StreamType.KCP_SRTP:
            self.part_json["streamSettings"] = self.load_template('kcp_srtp.json')

        elif self.stream_type == StreamType.KCP_WECHAT:
            self.part_json["streamSettings"] = self.load_template('kcp_wechat.json')

        elif self.stream_type == StreamType.KCP_DTLS:
            self.part_json["streamSettings"] = self.load_template('kcp_dtls.json')

        elif self.stream_type == StreamType.KCP_WG:
            self.part_json["streamSettings"] = self.load_template('kcp_wireguard.json')

        elif self.stream_type == StreamType.TCP:
            self.part_json["streamSettings"] = self.load_template('tcp.json')

        elif self.stream_type == StreamType.TCP_HOST:
            http = self.load_template('http.json')
            http["tcpSettings"]["header"]["request"]["headers"]["Host"] = kw["host"]
            self.part_json["streamSettings"] = http

        elif self.stream_type == StreamType.MTPROTO:
            mtproto = self.load_template('mtproto.json')
            self.to_mtproto(mtproto)

        elif self.stream_type == StreamType.SOCKS:
            socks = self.load_template('socks.json')
            tcp = self.load_template('tcp.json')
            socks["accounts"][0]["user"] = kw["user"]
            socks["accounts"][0]["pass"] = kw["pass"]
            self.part_json["settings"] = socks
            self.part_json["protocol"] = "socks"
            self.part_json["streamSettings"]=tcp

        elif self.stream_type == StreamType.SS:
            ss = self.load_template('ss.json')
            ss["port"] = self.part_json["port"]
            ss["settings"]["method"] = kw["method"]
            ss["settings"]["password"] = kw["password"]
            self.part_json = ss
        
        elif self.stream_type == StreamType.WS:
            ws = self.load_template('ws.json')
            salt = '/' + ''.join(random.sample(string.ascii_letters + string.digits, 8)) + '/'
            ws["wsSettings"]["path"] = salt
            ws["wsSettings"]["headers"]["Host"] = kw['host']
            self.part_json["streamSettings"]=ws

        elif self.stream_type == StreamType.H2:
            http2 = self.load_template('http2.json')
            salt = '/' + ''.join(random.sample(string.ascii_letters + string.digits, 8)) + '/'
            http2["httpSettings"]["path"]=salt
            self.part_json["streamSettings"]=http2

            # http2 tls的设置
            if security_backup != "tls" or not "certificates" in tls_settings_backup:
                from config_modify import tls
                tm = tls.TLSModifier(self.group_tag, self.group_index)
                tm.turn_on()
                self.save()
                return

        if (self.stream_type != StreamType.MTPROTO and origin_protocol != StreamType.MTPROTO 
           and self.stream_type != StreamType.SS and origin_protocol != StreamType.SS):
            self.part_json["streamSettings"]["security"] = security_backup
            self.part_json["streamSettings"]["tlsSettings"] = tls_settings_backup

        self.save()

class GroupWriter(Writer):
    def __init__(self, group_tag, group_index):
        super(GroupWriter, self).__init__(group_tag, group_index)
        self.locate_json()

    def write_port(self, new_port):
        self.part_json["port"] = int(new_port)
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
            if self.config["inboundDetour"] == None:
                self.config["inboundDetour"] = []
            self.config["inboundDetour"].append(dyn_json)
        else:
            dynamic_port_tag = self.part_json["settings"]["detour"]["to"]
            for index, detour_list in enumerate(self.config["inboundDetour"]):
                if "tag" in detour_list and detour_list["tag"] == dynamic_port_tag:
                    del self.config["inboundDetour"][index]
                    break
            if "detour" in self.part_json["settings"]:
                del self.part_json["settings"]["detour"]
        self.save()

    def write_tls(self, status = False, *, crt_file=None, key_file=None, domain=None):
        if status:
            tls_settings = self.load_template('tls_settings.json')
            tls_settings["certificates"][0]["certificateFile"] = crt_file
            tls_settings["certificates"][0]["keyFile"] = key_file
            self.part_json["streamSettings"]["security"] = "tls"
            self.part_json["streamSettings"]["tlsSettings"] = tls_settings

            with open('/usr/local/multi-v2ray/my_domain', 'w') as domain_file:
                domain_file.writelines(str(domain))
        else:
            if self.part_json["streamSettings"]["network"] == StreamType.H2.value:
                print("关闭tls同时也会关闭HTTP/2！\n")
                print("已重置为kcp utp传输方式, 若要其他方式请自行切换")
                self.part_json["streamSettings"] = self.load_template('kcp_utp.json')
            else:
                self.part_json["streamSettings"]["security"] = ""
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
    def __init__(self, group_tag = 'A', group_index=-1, client_index = 0):
        super(ClientWriter, self).__init__(group_tag, group_index)
        self.client_index = client_index
        self.locate_json()
        self.client_str = "clients" if self.part_json["protocol"] == "vmess" else "users"

    def write_aid(self, aid = 32):
        self.part_json["settings"][self.client_str][self.client_index]["alterId"] = int(aid)
        self.save()

    def write_uuid(self, new_uuid):
        self.part_json["settings"][self.client_str][self.client_index]["id"] = str(new_uuid)
        self.save()

    def write_email(self, email):
        if not "email" in self.part_json:
            self.part_json["settings"][self.client_str][self.client_index].update({"email": email})
        else:
            self.part_json["settings"][self.client_str][self.client_index]["email"] = email
        self.save()

class GlobalWriter(Writer):

    def __init__(self, group_list):
        super(GlobalWriter, self).__init__()
        self.group_list = group_list

    def write_ad(self, status = False):
        if status:
            self.config["routing"]["settings"]["rules"][0]["outboundTag"] = "blocked"
        else:
            self.config["routing"]["settings"]["rules"][0]["outboundTag"] = "direct"
        self.save()

    def write_stats(self, status = False):
        '''
        更改流量统计设置
        '''
        conf_rules = self.config["routing"]["settings"]["rules"]
        if status:
            stats_json = self.load_template('stats_settings.json')
            routing_rules = stats_json["routingRules"]
            del stats_json["routingRules"]

            has_rule = False
            for rules_list in conf_rules:
                if rules_list["outboundTag"] == "api":
                    has_rule = True
                    break
            if not has_rule:
                conf_rules.append(routing_rules)

            dokodemo_door = stats_json["dokodemoDoor"]
            del stats_json["dokodemoDoor"]
            #产生随机dokodemo_door的连接端口
            while True:
                random_port = random.randint(1000, 65535)
                if not port_is_use(random_port):
                    break
            dokodemo_door["port"] = random_port
            if self.config["inboundDetour"] == None:
                self.config["inboundDetour"]=[]

            has_door = False
            for detour_list in self.config["inboundDetour"]:
                if detour_list["protocol"] == "dokodemo-door" and detour_list["tag"] == "api":
                    has_door = True 
                    break
            if not has_door:
                self.config["inboundDetour"].append(dokodemo_door)

            #加入流量统计三件套
            self.config.update(stats_json)

            # 为各个组节点打上tag, 以便流量统计
            for group in self.group_list:
                if type(group) == Mtproto:
                    continue
                if group.tag == 'A':
                    self.config["inbound"].update({"tag":group.tag})
                else:
                    self.config["inboundDetour"][group.index].update({"tag": group.tag})
        else:
            # 删除用于统计流量的tag标签
            if "tag" in self.config["inbound"] and self.config["inbound"]["tag"] == "A":
                for group in self.group_list:
                    if type(group) == Mtproto:
                        continue
                    if group.tag == 'A':
                        del self.config["inbound"]["tag"]
                    else:
                        del self.config["inboundDetour"][group.index]["tag"]

            if "stats" in self.config:
                del self.config["stats"]
            if "api" in self.config:
                del self.config["api"]
            if "policy" in self.config:
                del self.config["policy"]

            for index,rules_list in enumerate(conf_rules):
                if rules_list["outboundTag"] == "api":
                    del conf_rules[index]

            if self.config["inboundDetour"]:
                for index, detour_list in enumerate(self.config["inboundDetour"]):
                    if detour_list["protocol"] == "dokodemo-door" and detour_list["tag"] == "api":
                        del self.config["inboundDetour"][index]
        self.save()

class NodeWriter(Writer):
    def create_new_port(self, newPort, protocol, **kw):
        # init new inbound
        server = self.load_template('server.json')
        new_inbound = server["inbound"]
        new_inbound["port"] = int(newPort)
        new_inbound["settings"]["clients"][0]["id"] = str(uuid.uuid1())
        if self.config["inboundDetour"] == None:
            self.config["inboundDetour"]=[]
        self.config["inboundDetour"].append(new_inbound)
        print("新增端口组成功!")
        self.save()

        reload_data = Loader()
        new_group_list = reload_data.profile.group_list
        stream_writer = StreamWriter(new_group_list[-1].tag, new_group_list[-1].index, protocol)
        stream_writer.write(**kw)

    def create_new_user(self, **kw):
        '''
        初始化时需传入group_tag, group_index参数, 自动调用父构造器来初始化
        '''
        self.locate_json()
        if self.part_json['protocol'] == 'socks':
            user = {"user": kw["user"], "pass": kw["pass"]}
            self.part_json["settings"]["accounts"].append(user)
            print("新建Socks5用户成功! user: %s, pass: %s" % (kw["user"], kw["pass"]))
        
        elif self.part_json['protocol'] == 'vmess' :
            new_uuid = uuid.uuid1()
            email_info = ""
            user = self.load_template('user.json')
            if "email" in kw and kw["email"] != "":
                user.update({"email":kw["email"]})
                email_info = ", email: " + kw["email"]
            user["id"]=str(new_uuid)
            self.part_json["settings"]["clients"].append(user)
            print("新建用户成功! uuid: %s, alterId: 32%s" % (str(new_uuid), email_info))

        self.save()

    def del_user(self, group, client_index):
        node = group.node_list[0]
        if len(group.node_list) == 1:
            if group.tag == 'A':
                print("inbound组只有一个用户，无法删除")
                return 
            else:
                if type(node) == Mtproto:
                    clean_mtproto_tag(self.config, group.index)
                print("当前inboundDetour组只有一个用户，整个节点组删除")
                del self.config["inboundDetour"][group.index]
                if len(self.config["inboundDetour"]) == 0:
                    self.config["inboundDetour"] == None
        elif type(node) == Vmess or type(node) == Socks:
            client_str = 'clients' if type(node) == Vmess else 'accounts'
            if group.tag == 'A':
                del self.config["inbound"]["settings"][client_str][client_index]
            else:
                del self.config["inboundDetour"][group.index]["settings"][client_str][client_index]

        print("删除用户成功!")
        self.save()

    def del_port(self, group):
        if group.tag == 'A':
            print("A组为inbound, 无法删除")
            return
        else:
            if type(group.node_list[0]) == Mtproto:
                clean_mtproto_tag(self.config, group.index)
            del self.config["inboundDetour"][group.index]
            if len(self.config["inboundDetour"]) == 0:
                self.config["inboundDetour"] == None
            print("删除端口成功!")
            self.save()