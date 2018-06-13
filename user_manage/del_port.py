#! /usr/bin/env python
# -*- coding: utf-8 -*-
import read_json
import write_json
import re

mul_user_conf = read_json.multiUserConf

choice=input("请输入要删除port的节点Group字母:")
choice=choice.upper()

if len(choice)==1 and re.match(r'[A-Z]', choice) and choice <= mul_user_conf[-1]['indexDict']['group']:
    
    print("你要删除的Group组所有节点信息:")
    for sin_user_conf in mul_user_conf:
        if sin_user_conf['indexDict']['group'] == choice:
            print(sin_user_conf)
    
    schoice = input("是否删除y/n：")
    if schoice == 'y':
        write_json.del_port(schoice)
    else:
        print("撤销删除")
else:
    print("输入有误，请检查是否为字母且范围中")