#! /usr/bin/env python
# -*- coding: utf-8 -*-
import read_json
import write_json
import re

mul_user_conf = read_json.multiUserConf

choice=input("请输入要改port的节点Group字母:")
choice=choice.upper()

if len(choice)==1 and re.match(r'[A-Z]', choice) and choice <= mul_user_conf[-1]['indexDict']['group']:
    write_json.create_new_user(choice)
else:
    print("输入有误，请检查是否为字母且范围中")