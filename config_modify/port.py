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
    for sin_user_conf in mul_user_conf:
        if sin_user_conf['indexDict']['group'] == choice:
            index_dict = sin_user_conf['indexDict']
            print ("当前组的端口为：%s" % str(sin_user_conf['port'])) 
            break

    print ("请输入新端口：")
    new_port=input()
    if (tool_box.is_number(new_port)):
        write_json.write_port(new_port, index_dict)
        print('端口修改成功！')
    else:
        print("输入错误，请检查是否为数字")
else:
    print("输入有误，请检查是否为字母且范围中")