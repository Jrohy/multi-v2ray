#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import sys

from ..util_core.writer import NodeWriter, GroupWriter
from ..util_core.group import Vmess, Socks, Mtproto, SS
from ..util_core.selector import GroupSelector, ClientSelector
from ..util_core.utils import StreamType, stream_list, is_email, clean_iptables, ColorStr

def new_port(new_stream=None):
    info = dict()
    if new_stream:
        correct_list = stream_list()
        if new_stream not in [x.value for x in correct_list]:
            print("input error! input -h or --help to get help")
            exit(-1)
        
        stream = list(filter(lambda stream:stream.value == new_stream, correct_list))[0]

        if stream == StreamType.SOCKS:
            user = input("please input socks user: ")
            password = input("please input socks password: ")
            if user == "" or password == "":
                print("socks user or password is null!!")
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
        print("random generate (srtp | wechat-video | utp | dtls) fake header, new protocol: {} \n".format(ColorStr.green(stream.value)))

    random_port = random.randint(1000, 65535)
    new_port = input("random generate port {}, enter to use, or input customize port: ".format(ColorStr.green(random_port)))

    if not new_port:
        new_port = str(random_port)

    if new_port.isnumeric():
        print("\nnew port: {} \n".format(new_port))
        nw = NodeWriter()
        nw.create_new_port(int(new_port), stream, **info)
    else:
        print ("\ninput error, please input number!!")

def new_user():
    gs = GroupSelector('user number')
    group = gs.group
    group_list = gs.group_list

    if group == None:
        exit(-1)
    else:
        email = ""
        if type(group.node_list[0]) == Vmess: 
            while True:
                is_duplicate_email=False

                email = input("input email to create user, or enter to pass: ")
                if email == "":
                    break
                if not is_email(email):
                    print("not email, please input again")
                    continue
                
                for loop_group in group_list:
                    for node in loop_group.node_list:
                        if node.user_info == None or node.user_info == '':
                            continue
                        elif node.user_info == email:
                            print("have same email, please input other")
                            is_duplicate_email = True
                            break              
                if not is_duplicate_email:
                    break

            nw = NodeWriter(group.tag, group.index)
            info = {'email': email}
            nw.create_new_user(**info)

        elif type(group.node_list[0]) == Socks:
            print("local group is socks, please input user and password to create user\n")
            user = input("please input socks user: ")
            password = input("please input socks password: ")
            if user == "" or password == "":
                print("socks user or password is null!!!")
                exit(-1)
            info = {"user":user, "pass": password}
            nw = NodeWriter(group.tag, group.index)
            nw.create_new_user(**info)

        elif type(group.node_list[0]) == Mtproto:
            print("\nMtproto protocol only support one user!!")

        elif type(group.node_list[0]) == SS:
            print("\nShadowsocks protocol only support one user, u can add new port to multiple SS!!")

def del_port():
    gs = GroupSelector('del port')
    group = gs.group

    if group == None:
        pass
    else:
        print("del group info: ")
        print(group)
        choice = input("delete?(y/n): ").lower()
        if choice == 'y':
            nw = NodeWriter()
            nw.del_port(group)
            clean_iptables(group.port)
        else:
            print("undo delete")

def del_user():
    cs = ClientSelector('del user')
    group = cs.group

    if group == None:
        pass
    else:
        client_index = cs.client_index
        print("del user info:")
        print(group.show_node(client_index))
        choice = input("delete?(y/n):").lower()
        if choice == 'y':
            if len(group.node_list) == 1:
                clean_iptables(group.port)
            nw = NodeWriter()
            nw.del_user(group, client_index)
        else:
            print("undo delete")