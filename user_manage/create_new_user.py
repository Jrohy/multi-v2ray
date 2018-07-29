#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import read_json
import write_json
import re
from base_util import tool_box

mul_user_conf = read_json.multiUserConf

length = len(mul_user_conf)

choice = 'A'

if length > 1:
    import server_info
    choice=input("请输入要创建user的节点Group字母:")
    choice=choice.upper()

if length == 1 or (len(choice)==1 and re.match(r'[A-Z]', choice) and choice <= mul_user_conf[-1]['indexDict']['group']):
    email = ""
    user_index=0
    for index, sin_user_conf in enumerate(mul_user_conf):
        if sin_user_conf['indexDict']['group'] == choice:
            user_index = index
            break
    protocol = mul_user_conf[user_index]["protocol"]
    if protocol == "vmess": 
        while True:
            is_duplicate_email=False

            email = input("是否输入email来新建用户, 回车直接跳过")
            if email == "":
                break
            if not tool_box.is_email(email):
                print("不是合格的email格式，请重新输入")
                continue
            
            for sin_user_conf in mul_user_conf:
                if sin_user_conf["email"] == "":
                    continue
                elif sin_user_conf["email"] == email:
                    print("已经有重复的email, 请重新输入")
                    is_duplicate_email = True
                    break
            
            if not is_duplicate_email:
                break
        write_json.create_new_user(choice, email=email)

    elif protocol == "socks":
        print("当前组为socks组, 请输入用户密码创建新的socks用户\n")
        user=input("请输入socks的用户名: ")
        password=input("请输入socks的密码: ")
        if user == "" or password == "":
            print("socks的用户名或者密码不能为空")
            exit()
        info = {"user":user, "pass": password}
        write_json.create_new_user(choice, **info)

    elif protocol == "mtproto":
        print("\n当前选择的组为MTProto协议, V2ray只支持该协议同组的第一个用户生效, 所以没必要新增用户!")

    elif protocol == "shadowsocks":
        print("\n当前选择的组为Shadowsocks协议, V2ray只支持ss协议一个用户一个端口, 想多用户请新增端口!")
else:
    print("输入有误，请检查是否为字母且范围中")