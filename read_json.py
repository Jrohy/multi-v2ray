#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import urllib.request

def dypJudge(conf_settings):
    conf_Dyp="关闭"
    if "detour" in conf_settings:
        dyp_AId=""
        dynamic_port_tag = conf_settings["detour"]["to"]
        for detour_list in conf_inboundDetour:
            if "tag" in detour_list and detour_list["tag"] == dynamic_port_tag:
                dyp_AId = detour_list["settings"]["default"]["alterId"]
                break
        conf_Dyp="开启,alterId为 %s" % dyp_AId
    return conf_Dyp

def read_sin_user(part_json, multi_user_conf, index_dict):
    conf_path=""
    conf_host=""
    conf_Dyp=""
    conf_stream_security=""
    conf_stream_header=""
    conf_stream_network=""
    conf_stream_header=""
    tls_domain=""
    global conf_ip
    global conf_inboundDetour

    protocol = part_json["protocol"]

    if "streamSettings" not in part_json and protocol != "mtproto" and protocol != "shadowsocks":
        return
    
    #节点组别分组
    if index_dict["inboundOrDetour"] == 1:
        number = ord(index_dict['group'])
        number += 1
        index_dict['group'] = chr(number)

    conf_settings = part_json["settings"]
    conf_Dyp=dypJudge(conf_settings)

    if protocol == "vmess" or protocol == "socks":
        conf_stream = part_json["streamSettings"]
        conf_stream_kcp_settings = conf_stream["kcpSettings"]
        conf_stream_network = conf_stream["network"]
        conf_stream_security = conf_stream["security"]

        conf_stream_tfo = None
        if "sockopt" in conf_stream:
            if "tcpFastOpen" in conf_stream["sockopt"]:
                if conf_stream["sockopt"]["tcpFastOpen"]:
                    conf_stream_tfo = "开启"
                else:
                    conf_stream_tfo = "关闭"

        if conf_stream["httpSettings"] != None:
            conf_path = conf_stream["httpSettings"]["path"]
        if conf_stream["wsSettings"] != None:
            conf_host = conf_stream["wsSettings"]["headers"]["Host"]
            conf_path = conf_stream["wsSettings"]["path"]
        if conf_stream["tcpSettings"] != None:
            conf_host = conf_stream["tcpSettings"]["header"]["request"]["headers"]["Host"]
        
        if (conf_stream_security == "tls"):
            with open('/usr/local/multi-v2ray/my_domain', 'r') as domain_file:
                content = domain_file.read()
                tls_domain = str(content)

        if conf_stream_network == "kcp" :
            if "header" in conf_stream_kcp_settings:
                conf_stream_header = conf_stream_kcp_settings["header"]["type"]
            else:
                conf_stream_header = "none"

    if protocol == "shadowsocks":
        sinUserConf={}
        sinUserConf['protocol']=protocol
        sinUserConf['port']=part_json["port"]
        sinUserConf['add']=(tls_domain if tls_domain != "" else conf_ip)
        email=""
        if "email" in conf_settings and conf_settings["email"]:
            email = conf_settings["email"]
        sinUserConf['email']=email
        sinUserConf['tls']=conf_stream_security
        sinUserConf['dyp']=conf_Dyp
        sinUserConf['id']=conf_settings["password"]
        sinUserConf['method']=conf_settings["method"]
        sinUserConf['indexDict']=index_dict.copy()
        multi_user_conf.append(sinUserConf)
        return

    elif protocol == "vmess":
        clients=conf_settings["clients"]
    elif protocol == "socks":
        clients=conf_settings["accounts"]
    elif protocol == "mtproto":
        clients=conf_settings["users"]

    for index,client in enumerate(clients):
        index_dict['clientIndex']=index
        email = ""
        if "email" in client and client["email"] != None:
            email = client["email"]
        sinUserConf={}
        sinUserConf['protocol']=protocol
        sinUserConf['port']=part_json["port"]
        sinUserConf['add']=(tls_domain if tls_domain != "" else conf_ip)
        sinUserConf['email']=(client["user"] if protocol == "socks" else email)
        sinUserConf['tls']=conf_stream_security
        sinUserConf['dyp']=conf_Dyp
        sinUserConf['tcpFastOpen']=conf_stream_tfo
        if protocol == "vmess":
            sinUserConf['v']="2"
            sinUserConf['ps']=""
            sinUserConf['aid']=client["alterId"]
            sinUserConf['type']=conf_stream_header
            sinUserConf['net']=conf_stream_network
            sinUserConf['path']=conf_path
            sinUserConf['host']=conf_host
            sinUserConf['id']=client["id"]
            sinUserConf['email']=email
        elif protocol == "socks":
            sinUserConf['id']=client["pass"]
        elif protocol == "mtproto":
            sinUserConf['id']=client["secret"]
        sinUserConf['indexDict']=index_dict.copy()

        multi_user_conf.append(sinUserConf)

with open('/etc/v2ray/config.json', 'r') as json_file:
    config = json.load(json_file)

#读取配置文件大框架
conf_inbound=config["inbound"]
conf_outbound=config["outbound"]
conf_inboundDetour=config["inboundDetour"]
conf_outboundDetour=config["outboundDetour"]
conf_dns=config["dns"]
conf_routing=config["routing"]

conf_stats = "开启" if "stats" in config else "关闭"

if conf_stats == "开启":
    for detour_list in conf_inboundDetour:
        if "protocol" in detour_list and detour_list["protocol"] == "dokodemo-door":
            conf_door_port = detour_list["port"]

#获取本机IP地址
my_ip = urllib.request.urlopen('http://api.ipify.org').read()
conf_ip = bytes.decode(my_ip)

multiUserConf=[]
#indexDict存储节点在json的索引，和节点代表的组别
#读取inbound节点
index_dict={"inboundOrDetour":0, "detourIndex":0, "clientIndex":0, "group":"A"}
read_sin_user(conf_inbound, multiUserConf, index_dict)

#读取inboundDetour节点
index_dict['inboundOrDetour']=1
if conf_inboundDetour != None:
    for index,detour_list in enumerate(conf_inboundDetour):
        index_dict['detourIndex']=index
        read_sin_user(detour_list, multiUserConf, index_dict)