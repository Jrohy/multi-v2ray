#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import urllib.request

def read_sin_user(part_json, multi_user_conf, index_dict):
    conf_path=""
    conf_host=""
    conf_Dyp=""
    conf_stream_security=""
    conf_stream_header=""
    global conf_ip
    global conf_inboundDetour

    if "streamSettings" not in part_json:
        return
    
    #节点组别分组
    if index_dict["inboundOrDetour"] == 1:
        number = ord(index_dict['group'])
        number += 1
        index_dict['group'] = chr(number)

    conf_settings = part_json[u"settings"]
    conf_stream = part_json[u"streamSettings"]
    conf_stream_kcp_settings = conf_stream[u"kcpSettings"]
    conf_stream_network = conf_stream[u"network"]
    conf_stream_security = conf_stream[u"security"]

    if "detour" in conf_settings:
        dyp_AId=""
        dynamic_port_tag = conf_settings[u"detour"][u"to"]
        for detour_list in conf_inboundDetour:
            if "tag" in detour_list and detour_list[u"tag"] == dynamic_port_tag:
                dyp_AId = detour_list[u"settings"][u"default"][u"alterId"]
                break
            conf_Dyp="开启,alterId为 %s" % dyp_AId
    else:
        conf_Dyp="关闭"
    
    if conf_stream[u"httpSettings"] != None:
        conf_path = conf_stream[u"httpSettings"][u"path"]
    if conf_stream[u"wsSettings"] != None:
        conf_host = conf_stream[u"wsSettings"][u"headers"][u"host"]
    if conf_stream[u"tcpSettings"] != None:
        conf_host = conf_stream[u"tcpSettings"][u"header"][u"request"][u"headers"][u"Host"]
    
    if (conf_stream_security == "tls"):
        with open('/usr/local/v2ray.fun/my_domain', 'r') as domain_file:
            content = domain_file.read()
            conf_ip = str(content)

    if conf_stream_network == "kcp" :
        if "header" in conf_stream_kcp_settings:
            conf_stream_header = conf_stream_kcp_settings[u"header"][u"type"]
        else:
            conf_stream_header = "none"

    clients=conf_settings[u"clients"]
    for index,client in enumerate(clients):
        index_dict['clientIndex']=index
        copy_index_dict = index_dict.copy()
        sinUserConf={}
        sinUserConf['v']="2"
        sinUserConf['add']=conf_ip
        sinUserConf['id']=client[u"id"]
        sinUserConf['aid']=client[u"alterId"]
        sinUserConf['port']=part_json[u"port"]
        sinUserConf['type']=conf_stream_header
        sinUserConf['net']=conf_stream_network
        sinUserConf['path']=conf_path
        sinUserConf['host']=conf_host
        sinUserConf['tls']=conf_stream_security
        sinUserConf['indexDict']=copy_index_dict
        sinUserConf['dyp']=conf_Dyp
        multi_user_conf.append(sinUserConf)

with open('/etc/v2ray/config.json', 'r') as json_file:
    config = json.load(json_file)

#读取配置文件大框架
conf_inbound=config[u"inbound"]
conf_outbound=config[u"outbound"]
conf_inboundDetour=config[u"inboundDetour"]
conf_outboundDetour=config[u"outboundDetour"]
conf_dns=config[u"dns"]
conf_routing=config[u"routing"]

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
