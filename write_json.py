#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import random
import string
import uuid
import read_json
import base_util.v2ray_util

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
def en_dyn_port(en, d_alterid=32):
    if en == 1:
        config[u"inbound"][u"settings"].update({u"detour":{u"to":"dynamicPort"}})
        with open('json_template/dyn_port.json', 'r') as dyn_port_file:
            dyn_json=json.load(dyn_port_file)
        dyn_json[u"settings"][u"default"][u"alterId"]=int(d_alterid)
        if config[u"inboundDetour"] == None:
            config[u"inboundDetour"]=[]
        config[u"inboundDetour"].append(dyn_json)
    else:
        for detour_list in config[u"inboundDetour"]:
            if "allocate" in detour_list:
                del detour_list
                break
        if "detour" in config[u"inbound"][u"settings"]:
            del config[u"inbound"][u"settings"][u"detour"]
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
        with open('json_template/tcp.json', 'r') as stream_file:
            tcp = json.load(stream_file)
        part_json[u"streamSettings"]=tcp

    if (network == "tcp" and para != "none"):
        with open('json_template/http.json', 'r') as stream_file:
            http = json.load(stream_file)
        http[u"tcpSettings"][u"header"][u"request"][u"headers"][u"Host"]=para
        part_json[u"streamSettings"]=http

    if (network == "h2"):
        with open('json_template/http2.json', 'r') as stream_file:
            http2 = json.load(stream_file)
        part_json[u"streamSettings"]=http2
        #随机生成8位的伪装path
        salt = '/' + ''.join(random.sample(string.ascii_letters + string.digits, 8)) + '/'
        part_json[u"streamSettings"][u"httpSettings"][u"path"]=salt
        if (security_backup != "tls" or not "certificates" in tls_settings_backup):
            v2ray_util.change_tls("on", index_dict)
            return

    if (network == "ws"):
        with open('json_template/ws.json', 'r') as stream_file:
            ws = json.load(stream_file)
        part_json[u"streamSettings"]=ws
        part_json[u"streamSettings"][u"wsSettings"][u"headers"][u"host"] = para

    if (network == "mkcp" and para=="none"):
        with open('json_template/kcp.json', 'r') as stream_file:
            kcp = json.load(stream_file)
        part_json[u"streamSettings"]=kcp
        
    if (network == "mkcp" and para=="kcp utp"):
        with open('json_template/kcp_utp.json', 'r') as stream_file:
            utp = json.load(stream_file)
        part_json[u"streamSettings"]=utp
        
    if (network == "mkcp" and para=="kcp srtp"):
        with open('json_template/kcp_srtp.json', 'r') as stream_file:
            srtp = json.load(stream_file)
        part_json[u"streamSettings"]=srtp
        
    if (network == "mkcp" and para=="kcp wechat-video"):
        with open('json_template/kcp_wechat.json', 'r') as stream_file:
            wechat = json.load(stream_file)
        part_json[u"streamSettings"]=wechat
    
    if (network == "mkcp" and para=="kcp dtls"):
        with open('json_template/kcp_dtls.json', 'r') as stream_file:
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
        with open('json_template/tls_settings.json', 'r') as tls_file:
            tls_settings=json.load(tls_file)
        tls_settings[u"certificates"][0][u"certificateFile"] = crt_file
        tls_settings[u"certificates"][0][u"keyFile"] = key_file
        part_json[u"streamSettings"][u"tlsSettings"] = tls_settings

        with open('my_domain', 'w') as domain_file:
            domain_file.writelines(str(domain))
        write()
    elif action == "off":
        if part_json[u"streamSettings"][u"network"] == "h2":
            print("关闭tls同时也会关闭HTTP/2\n")
            from base_util import random_stream
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
    with open('json_template/vmess.json', 'r') as vmess_file:
        vmess = json.load(vmess_file)
    with open('json_template/kcp_utp.json', 'r') as stream_file:
        utp = json.load(stream_file)
    
    vmess[u"streamSettings"]=utp
    vmess[u"port"]=newPort
    vmess[u"settings"][u"clients"][0][u"id"]=str(uuid.uuid1())
    if config[u"inboundDetour"] == None:
        config[u"inboundDetour"]=[]
    config[u"inboundDetour"].append(vmess)
    write()

#为某组新建用户
def create_new_user(group):
    new_uuid = uuid.uuid1()
    print("新建用户uuid为: %s, alterId 为 32") % str(new_uuid)
    with open('json_template/user.json', 'r') as userFile:
        user = json.load(userFile)
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
    write()

#删除组(端口)
def del_port(group):
    if group == 'A':
        print("A组为inbound, 无法删除")
        return
    else:
        multi_user_conf = read_json.multiUserConf
        for sin_user_conf in multi_user_conf:
            if sin_user_conf['indexDict']['group'] == group:
                detour_index=sin_user_conf['indexDict']['detourIndex']
                break

        del config[u"inboundDetour"][detour_index]

        if len(config[u"inboundDetour"]) == 0:
            config[u"inboundDetour"] == None
        write()

