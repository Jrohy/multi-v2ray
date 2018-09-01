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
    temp_user_conf=""
    for sin_user_conf in mul_user_conf:
        if sin_user_conf['indexDict']['group'] == choice:
            index_dict = sin_user_conf['indexDict']
            if sin_user_conf["protocol"] == "vmess":
                local_stream = sin_user_conf["net"] + " " + sin_user_conf["type"]
            elif sin_user_conf["protocol"] == "socks":
                local_stream="Socks5"
            elif sin_user_conf["protocol"] == "mtproto":
                local_stream="MTProto"
            elif sin_user_conf["protocol"] == "shadowsocks":
                local_stream="Shadowsocks"
            print ("当前组的传输方式为：%s" % local_stream) 
            temp_user_conf = sin_user_conf
            break

    stream_type = ("普通TCP", "HTTP伪装", "WebSocket流量", "普通mKCP", "mKCP + srtp", "mKCP + utp", "mKCP + wechat-video",
                   "mKCP + dtls", "mKCP + wireguard", "HTTP/2", "Socks5", "MTProto", "Shadowsocks")
    print ("")
    #选择新的传输方式
    for index, type_str in enumerate(stream_type):
        print("%d.%s" % (index + 1, type_str))

    new_stream_network=input()
    
    if not tool_box.is_number(new_stream_network):
        print("请输入数字！")
    else:
        new_stream_network = int(new_stream_network)
        if new_stream_network > 0 and new_stream_network <= len(stream_type):
            if (stream_type[new_stream_network - 1] == "MTProto" or stream_type[new_stream_network - 1] == "Shadowsocks") and temp_user_conf["tls"] == "tls":
                print("v2ray MTProto/Shadowsocks不支持https, 关闭tls成功!")
            v2ray_util.choice_stream(new_stream_network, index_dict)
            print("传输模式修改成功！")
        else:
            print("请输入符合范围的数字！")
else:
    print("输入有误，请检查是否为字母且范围中")