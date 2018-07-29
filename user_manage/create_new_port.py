#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import write_json
import random
import sys
from base_util import v2ray_util
from base_util import tool_box

protocol=""
info=dict()

if len(sys.argv) > 1:
    correct_protocol=("dtls", "wechat", "utp", "srtp", "mtproto", "socks","ss")
    protocol = sys.argv[1]
    if protocol not in correct_protocol:
        print("输入的参数无效! 输入-h 或者--help查看帮助")
        exit()

    if protocol == "socks":
        user=input("请输入socks的用户名: ")
        password=input("请输入socks的密码: ")
        if user == "" or password == "":
            print("socks的用户名或者密码不能为空")
            exit()
        info = {"user":user, "pass": password}
    elif protocol == "ss":
        method = v2ray_util.get_ss_method()
        password = v2ray_util.get_ss_password()
        info = {"method": method, "password": password}
else:
    salt_protocol=["dtls", "wechat", "utp", "srtp"]
    random.shuffle(salt_protocol)
    protocol=salt_protocol[0]
    print("随机一种 (srtp | wechat-video | utp | dtls) header伪装, 当前生成 %s" % protocol)

random_port = random.randint(1000, 65535)
new_port=input("产生随机端口%d, 回车直接以该端口新建Group, 否则输入自定义端口: " % random_port)

if not new_port:
    new_port = random_port

if tool_box.is_number(new_port):
    print("新端口为: %d \n" % int(new_port))
    write_json.create_new_port(new_port, protocol, **info)
else:
    print ("\n输入错误，请检查是否为数字")
