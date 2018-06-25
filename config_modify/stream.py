#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import read_json
import write_json
import re
from base_util import tool_box
from base_util import v2ray_util

mul_user_conf = read_json.multiUserConf

length = len(mul_user_conf)

choice = 'A'

if length > 1:
    import server_info
    choice=input("请输入要改传输方式的节点Group字母:")
    choice=choice.upper()

if length == 1 or (len(choice)==1 and re.match(r'[A-Z]', choice) and choice <= mul_user_conf[-1]['indexDict']['group']):
    for sin_user_conf in mul_user_conf:
        if sin_user_conf['indexDict']['group'] == choice:
            index_dict = sin_user_conf['indexDict']
            if sin_user_conf["protocol"] == "vmess":
                local_stream = sin_user_conf["net"] + " " + sin_user_conf["type"]
            elif sin_user_conf["protocol"] == "socks":
                local_stream="Socks5"
            print ("当前组的传输方式为：%s" % local_stream) 
            break

    print ("")
    #选择新的传输方式
    print ("请选择新的传输方式：")
    print ("1.普通TCP")
    print ("2.HTTP伪装")
    print ("3.WebSocket流量")
    print ("4.普通mKCP")
    print ("5.mKCP + srtp")
    print ("6.mKCP + utp")
    print ("7.mKCP + wechat-video")
    print ("8.mKCP + dtls")
    print ("9.HTTP/2")
    print ("10.Socks5")

    new_stream_network=input()
    
    if not tool_box.is_number(new_stream_network):
        print("请输入数字！")
        exit
    else:
        new_stream_network = int(new_stream_network)
        if new_stream_network > 0 and new_stream_network < 11:
            v2ray_util.choice_stream(new_stream_network, index_dict)
            print("传输模式修改成功！")
        else:
            print("请输入有效数字！")
            exit
else:
    print("输入有误，请检查是否为字母且范围中")