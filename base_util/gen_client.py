#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import read_json
from base_util import v2ray_util

#写客户端配置文件函数
def write_client_json():
    my_json_dump=json.dumps(client_config,indent=1)
    with open('/root/config.json', 'w') as write_json_file:
        write_json_file.writelines(my_json_dump)

#获取本机IP地址
myip = v2ray_util.get_ip()

#加载客户端配置模板
with open('/usr/local/v2ray.fun/json_template/client.json', 'r') as client_json_file:
    client_config = json.load(client_json_file)

#打开服务器端配置文件
with open('/etc/v2ray/config.json', 'r') as json_file:
    config = json.load(json_file)

mul_user_conf = read_json.multiUserConf

user_index=0

if len(mul_user_conf) > 1:
    import server_info
    choice=input("请输入要生成客户端json的节点序号:")
    if v2ray_util.is_number(choice) and choice > 0 and choice <= len(mul_user_conf):
        user_index = choice - 1
    else:
        print ("输入错误，请检查是否为数字和范围中")

#使用服务端配置来修改客户端模板
index_dict=mul_user_conf[user_index]['indexDict']
if index_dict['inboundOrDetour'] == 0:
    part_json = config[u"inbound"]
else:
    detour_index= index_dict['detourIndex']
    part_json = config[u"inboundDetour"][detour_index]

client_config[u"outbound"][u"settings"][u"vnext"][0][u"port"]=mul_user_conf[user_index]['port']
client_config[u"outbound"][u"settings"][u"vnext"][0][u"users"][0][u"id"]=mul_user_conf[user_index]['id']
client_config[u"outbound"][u"streamSettings"]=part_json[u"streamSettings"]
if mul_user_conf[user_index]['tls']== "":
    client_config[u"outbound"][u"settings"][u"vnext"][0][u"address"]=str(myip)
else:
    with open('/usr/local/v2ray.fun/my_domain', 'r') as domain_file:
        content = domain_file.read()
    client_config[u"outbound"][u"settings"][u"vnext"][0][u"address"] = str(content)
    client_config[u"outbound"][u"streamSettings"][u"network"] = mul_user_conf[user_index]['net']
    client_config[u"outbound"][u"streamSettings"][u"security"] = "tls"
    client_config[u"outbound"][u"streamSettings"][u"tlsSettings"] = {}
    client_config[u"outbound"][u"streamSettings"][u"httpSettings"] = part_json[u"streamSettings"][u"httpSettings"]

#写入客户端配置文件
write_client_json()
