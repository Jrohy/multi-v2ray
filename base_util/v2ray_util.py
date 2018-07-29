#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import write_json
import random
import socket
import os
import re
import string
from base_util import get_ssl
from base_util import tool_box

def get_ss_method():
    ss_method = ("aes-256-cfb", "aes-128-cfb", "chacha20", "chacha20-ietf", "aes-256-gcm", "aes-128-gcm", "chacha20-poly1305")
    print ("")
    #选择新的加密方式
    print ("请选择shadowsocks的加密方式：")
    for index, method in enumerate(ss_method):
        print ("%d.%s" % (index + 1, method))
    choice=input()
    choice = int(choice)
    if choice < 0 or choice > len(ss_method):
        print("输入错误，请检查是否符合范围中")
        exit()
    else:
        return ss_method[choice - 1]

def get_ss_password():
    random_pass = ''.join(random.sample(string.ascii_letters + string.digits, 16))
    new_pass =input("产生随机密码 %s , 回车直接使用该密码, 否则输入自定义密码: " % random_pass)

    if not new_pass:
        new_pass = random_pass
    return new_pass

def choice_stream(new_stream_network, index_dict):
    if(new_stream_network==1):
        write_json.write_stream_network("tcp", index_dict)
    elif(new_stream_network==2):
        print("请输入你想要为伪装的域名（不不不需要http）：")
        host=input()
        write_json.write_stream_network("tcp",index_dict, para=host)
    elif(new_stream_network==3):
        print("请输入你想要为伪装的域名（不不不需要http）：")
        host=input()
        write_json.write_stream_network("ws", index_dict, para=host)
    elif(new_stream_network==4):
        write_json.write_stream_network("mkcp", index_dict)
    elif(new_stream_network==5):
        write_json.write_stream_network("mkcp", index_dict, para = "kcp srtp")
    elif(new_stream_network==6):
        write_json.write_stream_network("mkcp", index_dict, para = "kcp utp")
    elif(new_stream_network==7):
        write_json.write_stream_network("mkcp", index_dict, para = "kcp wechat-video")
    elif(new_stream_network==8):
        write_json.write_stream_network("mkcp", index_dict, para = "kcp dtls")
    elif(new_stream_network==9):
        write_json.write_stream_network("h2", index_dict)
    elif(new_stream_network==10):
        user=input("请输入socks的用户名: ")
        password=input("请输入socks的密码: ")
        if user == "" or password == "":
            print("socks的用户名或者密码不能为空")
            exit()
        info = {"user":user, "pass": password}
        write_json.write_stream_network("socks", index_dict, **info)
    elif(new_stream_network==11):
        write_json.write_stream_network("mtproto", index_dict)
    elif(new_stream_network==12):
        method = get_ss_method()
        password = get_ss_password()
        info = {"method": method, "password": password}
        write_json.write_stream_network("shadowsocks", index_dict, **info)

#随机一种 (srtp | wechat-video | utp) header伪装, 默认inbound组的主用户
def random_kcp(index_dict={'inboundOrDetour': 0, 'detourIndex': 0, 'clientIndex': 0, 'group': 'A'}):
    kcp_list=('mKCP + srtp', 'mKCP + utp', 'mKCP + wechat-video', 'mKCP + dtls')
    choice = random.randint(5,8)
    print("随机一种 (srtp | wechat-video | utp | dtls) header伪装, 当前生成 %s" % kcp_list[choice - 5])
    print()
    choice_stream(choice, index_dict)

def change_tls(yn, index_dict):
    if yn == "on":
        print("\n请将您的域名解析到本VPS的IP地址，否则程序会出错！！\n")
        local_ip = tool_box.get_ip()
        print("本机器IP地址为：" + local_ip + "\n")
        input_domain=str(input("请输入您绑定的域名："))
        try:
            input_ip = socket.gethostbyname(input_domain)
        except Exception:
            print("\n域名检测错误!!!\n")
            return
        if input_ip != local_ip:
            print("\n输入的域名与本机ip不符!!!\n")
            return

        print("")
        print("正在获取SSL证书，请稍等。")
        get_ssl.getssl(input_domain)
        write_json.write_tls("on",input_domain, index_dict)
    elif yn == "off":
        write_json.write_tls("off","", index_dict)
        
    print("\n操作完成！\n")

def get_stats(type, meta_info, door_port, is_reset = False):
    is_reset = "true" if is_reset else "false"

    stats_cmd = "cd /usr/bin/v2ray && ./v2ctl api --server=127.0.0.1:%s StatsService.GetStats 'name: \"%s>>>%s>>>traffic>>>%s\" reset: %s'"
    type_tag = ("user" if type == 0 else "inbound")

    stats_real_cmd = stats_cmd % (str(door_port), type_tag, meta_info, "downlink", is_reset)
    downlink_result = os.popen(stats_real_cmd).readlines()
    if downlink_result and len(downlink_result) == 5:
        re_result = re.findall(r"\d+", downlink_result[2])
        if not re_result:
            print("当前无流量数据，请使用流量片刻再来查看统计!")
            return
        downlink_value = int(re_result[0])
        print("\033[36m")
        print("\ndownlink: " + tool_box.bytes_2_human_readable(downlink_value, 2) + "\n")

    stats_real_cmd = stats_cmd % (str(door_port), type_tag, meta_info, "uplink", is_reset)
    uplink_result = os.popen(stats_real_cmd).readlines()
    if uplink_result and len(uplink_result) == 5:
        re_result = re.findall(r"\d+", uplink_result[2])
        uplink_value = int(re_result[0])
        print("uplink: " + tool_box.bytes_2_human_readable(uplink_value, 2) + "\n")
        print("total: " + tool_box.bytes_2_human_readable(downlink_value + uplink_value, 2) + "\n")
        print("\033[0m")