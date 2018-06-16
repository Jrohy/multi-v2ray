#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import read_json
import write_json
import re

mul_user_conf = read_json.multiUserConf

length = len(mul_user_conf)

choice = 'A'

if length > 1:
    import server_info
    choice=input("请输入要改port的节点Group字母:")
    choice=choice.upper()

if length == 1 or (len(choice)==1 and re.match(r'[A-Z]', choice) and choice <= mul_user_conf[-1]['indexDict']['group']):
    write_json.create_new_user(choice)
else:
    print("输入有误，请检查是否为字母且范围中")