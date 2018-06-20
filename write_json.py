#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import random
import string
import uuid
import read_json
from base_util import tool_box

#打开配置文件
with open('/etc/v2ray/config.json', 'r') as json_file:
    config = json.load(json_file)

#写入配置文件
def write():
    my_json_dump=json.dumps(config,indent=1)
    with open('/etc/v2ray/config.json', 'w') as write_json_file:
        write_json_file.writelines(my_json_dump)

#inbound级别定位json
def locate_json(index_dict):
    if index_dict['inboundOrDetour'] == 0:
        part_json = config[u"inbound"]
    else:
        detour_index= index_dict['detourIndex']
        part_json = config[u"inboundDetour"][detour_index]
    return part_json

#更改动态端口
def en_dyn_port(en, index_dict, d_alterid=32):
    part_json = locate_json(index_dict)
    if en == 1:
        short_uuid = str(uuid.uuid1())[0:7]
        dynamic_port_tag = "dynamicPort" + short_uuid
        part_json[u"settings"].update({u"detour":{u"to":dynamic_port_tag}})
        with open('/usr/local/v2ray.fun/json_template/dyn_port.json', 'r') as dyn_port_file:
            dyn_json=json.load(dyn_port_file)
        dyn_json[u"settings"][u"default"][u"alterId"]=int(d_alterid)
        dyn_json[u"tag"]=dynamic_port_tag
        if config[u"inboundDetour"] == None:
            config[u"inboundDetour"]=[]
        config[u"inboundDetour"].append(dyn_json)
    else:
        dynamic_port_tag = part_json[u"settings"][u"detour"][u"to"]
        for detour_list in config[u"inboundDetour"]:
            if "tag" in detour_list and detour_list[u"tag"] == dynamic_port_tag:
                del detour_list
                break
        if "detour" in part_json[u"settings"]:
            del part_json[u"settings"][u"detour"]
    write()

#更改alterId
def write_alterid(alterid, index_dict):
    client_index = index_dict['clientIndex']
    part_json = locate_json(index_dict)
    part_json[u"settings"][u"clients"][client_index][u"alterId"]=int(alterid)
    write()

#更改端口
def write_port(my_port, index_dict):
    part_json = locate_json(index_dict)
    part_json[u"port"]=int(my_port)
    write()

#更改UUID
def write_uuid(my_uuid, index_dict):
    client_index = index_dict['clientIndex']
    part_json = locate_json(index_dict)
    part_json[u"settings"][u"clients"][client_index][u"id"]=str(my_uuid)
    write()

#更改底层传输设置
def write_stream_network(network, para, index_dict):
    part_json = locate_json(index_dict)
    security_backup = part_json[u"streamSettings"][u"security"]
    tls_settings_backup = part_json[u"streamSettings"][u"tlsSettings"]

    if (network == "tcp" and para == "none"):
        with open('/usr/local/v2ray.fun/json_template/tcp.json', 'r') as stream_file:
            tcp = json.load(stream_file)
        part_json[u"streamSettings"]=tcp

    if (network == "tcp" and para != "none"):
        with open('/usr/local/v2ray.fun/json_template/http.json', 'r') as stream_file:
            http = json.load(stream_file)
        http[u"tcpSettings"][u"header"][u"request"][u"headers"][u"Host"]=para
        part_json[u"streamSettings"]=http

    if (network == "h2"):
        with open('/usr/local/v2ray.fun/json_template/http2.json', 'r') as stream_file:
            http2 = json.load(stream_file)
        part_json[u"streamSettings"]=http2
        #随机生成8位的伪装path
        salt = '/' + ''.join(random.sample(string.ascii_letters + string.digits, 8)) + '/'
        part_json[u"streamSettings"][u"httpSettings"][u"path"]=salt
        if (security_backup != "tls" or not "certificates" in tls_settings_backup):
            from base_util import v2ray_util
            v2ray_util.change_tls("on", index_dict)
            return

    if (network == "ws"):
        with open('/usr/local/v2ray.fun/json_template/ws.json', 'r') as stream_file:
            ws = json.load(stream_file)
        part_json[u"streamSettings"]=ws
        part_json[u"streamSettings"][u"wsSettings"][u"headers"][u"host"] = para

    if (network == "mkcp" and para=="none"):
        with open('json_template/kcp.json', 'r') as stream_file:
            kcp = json.load(stream_file)
        part_json[u"streamSettings"]=kcp
        
    if (network == "mkcp" and para=="kcp utp"):
        with open('/usr/local/v2ray.fun/json_template/kcp_utp.json', 'r') as stream_file:
            utp = json.load(stream_file)
        part_json[u"streamSettings"]=utp
        
    if (network == "mkcp" and para=="kcp srtp"):
        with open('/usr/local/v2ray.fun/json_template/kcp_srtp.json', 'r') as stream_file:
            srtp = json.load(stream_file)
        part_json[u"streamSettings"]=srtp
        
    if (network == "mkcp" and para=="kcp wechat-video"):
        with open('/usr/local/v2ray.fun/json_template/kcp_wechat.json', 'r') as stream_file:
            wechat = json.load(stream_file)
        part_json[u"streamSettings"]=wechat
    
    if (network == "mkcp" and para=="kcp dtls"):
        with open('/usr/local/v2ray.fun/json_template/kcp_dtls.json', 'r') as stream_file:
            dtls = json.load(stream_file)
        part_json[u"streamSettings"]=dtls
    
    part_json[u"streamSettings"][u"security"] = security_backup
    part_json[u"streamSettings"][u"tlsSettings"] = tls_settings_backup
    write()

#更改TLS设置
def write_tls(action, domain, index_dict):
    part_json = locate_json(index_dict)
    if action == "on":
        part_json[u"streamSettings"][u"security"] = "tls"
        crt_file = "/root/.acme.sh/" + domain +"_ecc"+ "/fullchain.cer"
        key_file = "/root/.acme.sh/" + domain +"_ecc"+ "/"+ domain +".key"
        with open('/usr/local/v2ray.fun/json_template/tls_settings.json', 'r') as tls_file:
            tls_settings=json.load(tls_file)
        tls_settings[u"certificates"][0][u"certificateFile"] = crt_file
        tls_settings[u"certificates"][0][u"keyFile"] = key_file
        part_json[u"streamSettings"][u"tlsSettings"] = tls_settings

        with open('/usr/local/v2ray.fun/my_domain', 'w') as domain_file:
            domain_file.writelines(str(domain))
    elif action == "off":
        if part_json[u"streamSettings"][u"network"] == "h2":
            print("关闭tls同时也会关闭HTTP/2！\n")
            print("已重置为kcp utp传输方式, 若要其他方式请自行切换")
            with open('/usr/local/v2ray.fun/json_template/kcp_utp.json', 'r') as stream_file:
                utp = json.load(stream_file)
            part_json[u"streamSettings"] = utp
        else:
            part_json[u"streamSettings"][u"security"] = ""
            part_json[u"streamSettings"][u"tlsSettings"] = {}
    write()

#更改广告拦截功能
def write_ad(action):
    if action == "on":
        config[u"routing"][u"settings"][u"rules"][0][u"outboundTag"] = "blocked"
    else:
        config[u"routing"][u"settings"][u"rules"][0][u"outboundTag"] = "direct"
    write()

#创建新的端口(组)
def create_new_port(newPort):
    print("默认选择kcp utp传输方式创建, 若要其他方式请自行切换")
    with open('/usr/local/v2ray.fun/json_template/vmess.json', 'r') as vmess_file:
        vmess = json.load(vmess_file)
    with open('/usr/local/v2ray.fun/json_template/kcp_utp.json', 'r') as stream_file:
        utp = json.load(stream_file)
    
    vmess[u"streamSettings"]=utp
    vmess[u"port"]=newPort
    vmess[u"settings"][u"clients"][0][u"id"]=str(uuid.uuid1())
    if config[u"inboundDetour"] == None:
        config[u"inboundDetour"]=[]
    config[u"inboundDetour"].append(vmess)
    print("新增端口组成功!")
    write()

#为某组新建用户
def create_new_user(group, email=""):
    new_uuid = uuid.uuid1()
    email_info = ""
    with open('/usr/local/v2ray.fun/json_template/user.json', 'r') as userFile:
        user = json.load(userFile)
    if email != "":
        user.update({u"email":email})
        email_info = ", email: " + email
    user[u"id"]=str(new_uuid)
    multi_user_conf = read_json.multiUserConf
    detour_index=0
    for sin_user_conf in multi_user_conf:
        if sin_user_conf['indexDict']['group'] == group:
            detour_index = sin_user_conf['indexDict']['detourIndex']
            break
    if group == "A":
        config[u"inbound"][u"settings"][u"clients"].append(user)
    else:
        config[u"inboundDetour"][detour_index][u"settings"][u"clients"].append(user)
    
    print("新建用户成功! uuid: %s, alterId: 32%s" % (str(new_uuid), email_info))
    write()

#删除用户
def del_user(index):
    multi_user_conf = read_json.multiUserConf
    index_dict = multi_user_conf[index]['indexDict']
    group = index_dict['group']

    #统计当前操作记录所在组的user数量
    count=0
    for sin_user_conf in multi_user_conf:
        if sin_user_conf['indexDict']['group'] == group:
            count += 1
    
    if group == 'A':
        if count == 1:
            print("inbound组只有一个用户，无法删除")
            return
        del config[u"inbound"][u"settings"][u"clients"][index_dict['clientIndex']]
    else:
        if count == 1:
            print("当前inboundDetour组只有一个用户，整个节点组删除")
            del config[u"inboundDetour"][index_dict['detourIndex']]
            if len(config[u"inboundDetour"]) == 0:
                config[u"inboundDetour"] == None
        else:
            del config[u"inboundDetour"][index_dict['detourIndex']][u"settings"][u"clients"][index_dict['clientIndex']]
    print("删除用户成功!")
    write()

#删除组(端口)
def del_port(group):
    if group == 'A':
        print("A组为inbound, 无法删除")
        return
    else:
        multi_user_conf = read_json.multiUserConf
        detour_index = 0
        for sin_user_conf in multi_user_conf:
            if sin_user_conf['indexDict']['group'] == group:
                detour_index=sin_user_conf['indexDict']['detourIndex']
                break

        del config[u"inboundDetour"][detour_index]

        if len(config[u"inboundDetour"]) == 0:
            config[u"inboundDetour"] == None
        print("删除端口成功!")
        write()

#更改流量统计设置
def write_stats(action, multi_user_conf):
    conf_rules = config[u"routing"][u"settings"][u"rules"]
    if action == "on":
        with open('/usr/local/v2ray.fun/json_template/stats_settings.json', 'r') as stats_file:
            stats_json=json.load(stats_file)
        routing_rules = stats_json[u"routingRules"]
        del stats_json[u"routingRules"]

        for index_x, one_rule in enumerate(conf_rules):
            if "ip" in one_rule:
                for index_y, one_ip in enumerate(one_rule["ip"]):
                    if one_ip == "127.0.0.0/8":
                        del conf_rules[index_x]["ip"][index_y]
                        break
                break

        conf_rules.append(routing_rules)

        dokodemo_door = stats_json[u"dokodemoDoor"]
        del stats_json[u"dokodemoDoor"]
        #产生随机dokodemo_door的连接端口
        while True:
            random_port = random.randint(1000, 65535)
            if tool_box.port_is_open(random_port):
                break
        dokodemo_door[u"port"] = random_port
        if config[u"inboundDetour"] == None:
            config[u"inboundDetour"]=[]
        config[u"inboundDetour"].append(dokodemo_door)

        config.update(stats_json)

        last_group = "Z"
        for sin_user_conf in multi_user_conf:
            index_dict = sin_user_conf["indexDict"]
            group = index_dict["group"]
            if last_group == group:
                continue
            if group == 'A':
                config[u"inbound"].update({u"tag":group})
            else:
                config[u"inboundDetour"][index_dict["detourIndex"]].update({u"tag":group})
            last_group = group

    elif action == "off":
        if "stats" in config:
            del config[u"stats"]
        if "api" in config:
            del config[u"api"]
        if "policy" in config:
            del config[u"policy"]
        if config[u"inboundDetour"]:
            for index, detour_list in enumerate(config[u"inboundDetour"]):
                if detour_list[u"protocol"] == "dokodemo-door" and detour_list[u"tag"] == "api":
                    del config[u"inboundDetour"][index]
                    break

        for index,rules_list in enumerate(conf_rules):
            if rules_list[u"outboundTag"] == "api":
                del conf_rules[index]
                break
        
        if "tag" in config[u"inbound"] and config[u"inbound"][u"tag"] == "A":
            last_group = "Z"
            for sin_user_conf in multi_user_conf:
                index_dict = sin_user_conf["indexDict"]
                group = index_dict["group"]
                if last_group == group:
                    continue
                if group == 'A':
                    del config[u"inbound"][u"tag"]
                else:
                    del config[u"inboundDetour"][index_dict["detourIndex"]][u"tag"]
                last_group = group
    write()