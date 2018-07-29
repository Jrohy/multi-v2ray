#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import read_json
import write_json
import re
import sys
from base_util import v2ray_util

# 外部传参来决定修改哪种, 默认修改method
ss_modify="method"

if len(sys.argv) > 1:
    correct_way=("method", "password")
    ss_modify = sys.argv[1]
    if ss_modify not in correct_way:
        print("传参有误!")
        exit()

mul_user_conf = read_json.multiUserConf

length = len(mul_user_conf)

choice = 'A'

if length > 1:
    import server_info
    choice=input("请输入要改shadowsocks加密方式/密码的节点Group字母:")
    choice=choice.upper()

if length == 1 or (len(choice)==1 and re.match(r'[A-Z]', choice) and choice <= mul_user_conf[-1]['indexDict']['group']):
    select_user=""
    for sin_user_conf in mul_user_conf:
        if sin_user_conf['indexDict']['group'] == choice:
            index_dict = sin_user_conf['indexDict']
            if sin_user_conf["protocol"] != "shadowsocks":
                print("\n当前选择组不是Shadowsocks协议!\n")
                exit()
            select_user = sin_user_conf
            break
    if ss_modify == "method":
        method = v2ray_util.get_ss_method()
        write_json.write_ss_method(method, select_user['indexDict'])
    elif ss_modify == "password":
        password = v2ray_util.get_ss_password()
        write_json.write_ss_password(password, select_user['indexDict'])
    print("修改Shadowsocks %s成功!\n" % ss_modify)
    
else:
    print("输入有误，请检查是否为字母且范围中")