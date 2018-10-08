#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import sys

from config_modify import ss
from writer import NodeWriter, StreamType

info = dict()

if len(sys.argv) > 1:
    protocol_list = [
        ("wireguard", StreamType.KCP_WG), 
        ("dtls", StreamType.KCP_DTLS), 
        ("wechat", StreamType.KCP_WECHAT), 
        ("utp", StreamType.KCP_UTP), 
        ("srtp", StreamType.KCP_SRTP), 
        ("mtproto", StreamType.MTPROTO), 
        ("socks", StreamType.SOCKS),
        ("ss", StreamType.SS)
    ]
    protocol = sys.argv[1]
    correct = False
    for x in protocol_list:
        if x[0] == protocol:
            correct = True
            protocol = x[1]
    if not correct:
        print("输入的参数无效! 输入-h 或者--help查看帮助")
        exit(-1)

    if protocol == StreamType.SOCKS:
        user = input("请输入socks的用户名: ")
        password = input("请输入socks的密码: ")
        if user == "" or password == "":
            print("socks的用户名或者密码不能为空")
            exit(-1)
        info = {"user":user, "pass": password}
    elif protocol == StreamType.SS:
        sf = ss.SSFactory()
        info = {"method": sf.get_method(), "password": sf.get_password()}
else:
    salt_protocol = [StreamType.KCP_DTLS, StreamType.KCP_WECHAT, StreamType.KCP_UTP, StreamType.KCP_SRTP]
    random.shuffle(salt_protocol)
    protocol = salt_protocol[0]
    print("随机一种 (srtp | wechat-video | utp | dtls) header伪装, 当前生成 {} \n".format(protocol.value))

random_port = random.randint(1000, 65535)
new_port = input("产生随机端口{}, 回车直接以该端口新建Group, 否则输入自定义端口: ".format(random_port))

if not new_port:
    new_port = str(random_port)

if new_port.isnumeric():
    print("\n新端口为: {} \n".format(new_port))
    nw = NodeWriter()
    nw.create_new_port(int(new_port), protocol, **info)
else:
    print ("\n输入错误，请检查是否为数字")