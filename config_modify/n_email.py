#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import read_json
import write_json
from base_util import tool_box

mul_user_conf = read_json.multiUserConf

length = len(mul_user_conf)

choice = 1

if length > 1:
    import server_info
    choice=input("请输入要改email的节点序号数字:")
    if not tool_box.is_number(choice):
        print("输入错误，请检查是否为数字")
        exit()
    choice = int(choice)

if length == 1 or (choice > 0 and choice <= len(mul_user_conf)):
    if mul_user_conf[choice - 1]["protocol"] == "socks":
        print("Socks5节点 不支持写入email!")
        exit()
    print ("当前节点email为：%s" % mul_user_conf[choice - 1]['email'])
    email = ""
    while True:
        is_duplicate_email=False
        email = input("请输入新的email地址: ")
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
    if email != "":
        write_json.write_email(email, mul_user_conf[choice - 1]['indexDict'], mul_user_conf[choice - 1]["protocol"])
        print("修改email成功!")
else:
    print ("输入错误，请检查是否符合范围中")