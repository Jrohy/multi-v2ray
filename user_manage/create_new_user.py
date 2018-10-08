#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from utils import is_email
from group import Vmess, Socks, Mtproto, SS
from writer import GroupWriter, NodeWriter
from selector import GroupSelector

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