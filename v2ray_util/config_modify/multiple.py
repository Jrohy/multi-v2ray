#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import sys

from ..util_core.writer import NodeWriter, GroupWriter
from ..util_core.group import Vmess, Socks, Mtproto, SS
from ..util_core.selector import GroupSelector, ClientSelector
from ..util_core.utils import StreamType, stream_list, is_email, clean_iptables

def new_port(new_stream=None):
    info = dict()
    if new_stream:
        correct_list = stream_list()
        if new_stream not in [x.value for x in correct_list]:
            print("输入的参数无效! 输入-h 或者--help查看帮助")
            exit(-1)
        
        stream = list(filter(lambda stream:stream.value == new_stream, correct_list))[0]

        if stream == StreamType.SOCKS:
            user = input("请输入socks的用户名: ")
            password = input("请输入socks的密码: ")
            if user == "" or password == "":
                print("socks的用户名或者密码不能为空")
                exit(-1)
            info = {"user":user, "pass": password}
        elif stream == StreamType.SS:
            from .ss import SSFactory
            sf = SSFactory()
            info = {"method": sf.get_method(), "password": sf.get_password()}
    else:
        salt_stream = [StreamType.KCP_DTLS, StreamType.KCP_WECHAT, StreamType.KCP_UTP, StreamType.KCP_SRTP]
        random.shuffle(salt_stream)
        stream = salt_stream[0]
        print("随机一种 (srtp | wechat-video | utp | dtls) header伪装, 当前生成 {} \n".format(stream.value))

    random_port = random.randint(1000, 65535)
    new_port = input("产生随机端口{}, 回车直接以该端口新建Group, 否则输入自定义端口: ".format(random_port))

    if not new_port:
        new_port = str(random_port)

    if new_port.isnumeric():
        print("\n新端口为: {} \n".format(new_port))
        nw = NodeWriter()
        nw.create_new_port(int(new_port), stream, **info)
    else:
        print ("\n输入错误，请检查是否为数字")

def new_user():
    gs = GroupSelector('user数量')
    group = gs.group
    group_list = gs.group_list

    if group == None:
        exit(-1)
    else:
        email = ""
        if type(group.node_list[0]) == Vmess: 
            while True:
                is_duplicate_email=False

                email = input("是否输入email来新建用户, 回车直接跳过: ")
                if email == "":
                    break
                if not is_email(email):
                    print("不是合格的email格式，请重新输入")
                    continue
                
                for loop_group in group_list:
                    for node in loop_group.node_list:
                        if node.user_info == None or node.user_info == '':
                            continue
                        elif node.user_info == email:
                            print("已经有重复的email, 请重新输入")
                            is_duplicate_email = True
                            break              
                if not is_duplicate_email:
                    break

            nw = NodeWriter(group.tag, group.index)
            info = {'email': email}
            nw.create_new_user(**info)

        elif type(group.node_list[0]) == Socks:
            print("当前组为socks组, 请输入用户密码创建新的socks用户\n")
            user = input("请输入socks的用户名: ")
            password = input("请输入socks的密码: ")
            if user == "" or password == "":
                print("socks的用户名或者密码不能为空")
                exit(-1)
            info = {"user":user, "pass": password}
            nw = NodeWriter(group.tag, group.index)
            nw.create_new_user(**info)

        elif type(group.node_list[0]) == Mtproto:
            print("\n当前选择的组为MTProto协议, V2ray只支持该协议同组的第一个用户生效, 所以没必要新增用户!")

        elif type(group.node_list[0]) == SS:
            print("\n当前选择的组为Shadowsocks协议, V2ray只支持ss协议一个用户一个端口, 想多用户请新增端口!")

def del_port():
    gs = GroupSelector('删除port')
    group = gs.group

    if group == None:
        pass
    else:
        print("你要删除的Group组所有节点信息: ")
        print(group)
        choice = input("是否删除y/n：").lower()
        if choice == 'y':
            nw = NodeWriter()
            nw.del_port(group)
            clean_iptables(group.port)
        else:
            print("撤销删除")

def del_user():
    cs = ClientSelector('删除user')
    group = cs.group

    if group == None:
        pass
    else:
        client_index = cs.client_index
        print("你选择的user信息:")
        print(group.show_node(client_index))
        choice = input("是否删除y/n：").lower()
        if choice == 'y':
            if len(group.node_list) == 1:
                clean_iptables(group.port)
            nw = NodeWriter()
            nw.del_user(group, client_index)
        else:
            print("撤销删除")