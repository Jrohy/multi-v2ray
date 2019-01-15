#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ..util_core.group import Socks
from ..util_core.writer import ClientWriter
from ..util_core.selector import ClientSelector
from ..util_core.utils import is_email

cs = ClientSelector('修改email')
group = cs.group

if group == None:
    pass
elif type(group.node_list[0]) == Socks:
    print("Socks5节点 不支持写入email!")
else:
    client_index = cs.client_index
    group_list = cs.group_list
    print ("当前节点email为：{}".format(group.node_list[client_index].user_info))
    email = ""
    while True:
        is_duplicate_email=False
        email = input("请输入新的email地址: ")
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

    if email != "":
        cw = ClientWriter(group.tag, group.index, client_index)
        cw.write_email(email)
        print("修改email成功!")