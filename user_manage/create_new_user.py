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
    choice=input("请输入要改port的节点Group字母:")
    choice=choice.upper()

if length == 1 or (len(choice)==1 and re.match(r'[A-Z]', choice) and choice <= mul_user_conf[-1]['indexDict']['group']):
    email = ""
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
    write_json.create_new_user(choice, email)
else:
    print("输入有误，请检查是否为字母且范围中")