#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import read_json
from base_util import tool_box

#写客户端配置文件函数
def write_client_json():
    my_json_dump=json.dumps(client_config,indent=1)
    with open('/root/config.json', 'w') as write_json_file:
        write_json_file.writelines(my_json_dump)

#获取本机IP地址
myip = tool_box.get_ip()

#打开服务器端配置文件
with open('/etc/v2ray/config.json', 'r') as json_file:
    config = json.load(json_file)

mul_user_conf = read_json.multiUserConf

user_index=0

if len(mul_user_conf) > 1:
    import server_info
    choice=input("请输入要生成客户端json的节点序号:")
    if tool_box.is_number(choice):
        choice = int(choice)
        if choice > 0 and choice <= len(mul_user_conf):
            user_index = choice - 1
        else:
            print ("输入错误，请检查数字是否在范围中")
            exit
    else:
        print("输入错误,请检查是否为数字")
        exit

index_dict = mul_user_conf[user_index]['indexDict']

protocol = mul_user_conf[user_index]['protocol']

if index_dict['inboundOrDetour'] == 0:
    part_json = config["inbound"]
else:
    detour_index= index_dict['detourIndex']
    part_json = config["inboundDetour"][detour_index]

#加载客户端配置模板
if protocol == "vmess":
    with open('/usr/local/v2ray.fun/json_template/client.json', 'r') as client_json_file:
        client_config = json.load(client_json_file)
    user_json=client_config["outbound"]["settings"]["vnext"][0]
    user_json["users"][0]["id"]=mul_user_conf[user_index]['id']
    user_json["users"][0]["alterId"]=mul_user_conf[user_index]['aid']
elif protocol == "socks":
    with open('/usr/local/v2ray.fun/json_template/client_socks.json', 'r') as client_json_file:
        client_config = json.load(client_json_file)
    user_json=client_config["outbound"]["settings"]["servers"][0]
    user_json["users"][0]["user"]=mul_user_conf[user_index]['email']
    user_json["users"][0]["pass"]=mul_user_conf[user_index]['id']

user_json["port"]=int(mul_user_conf[user_index]['port'])
client_config["outbound"]["streamSettings"]=part_json["streamSettings"]

if mul_user_conf[user_index]['tls']== "":
    user_json["address"]=str(myip)
else:
    with open('/usr/local/v2ray.fun/my_domain', 'r') as domain_file:
        content = domain_file.read()
    user_json["address"] = str(content)
    client_config["outbound"]["streamSettings"]["tlsSettings"] = {}

#写入客户端配置文件
write_client_json()
