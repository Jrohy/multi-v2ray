#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from writer import NodeWriter
from selector import ClientSelector

cs = ClientSelector('删除user')
client_index = cs.client_index
group = cs.group

if group == None:
    exit(-1)
else:
    print("你选择的user信息:")
    print(group.show_node(client_index))
    choice = input("是否删除y/n：").lower()
    if choice == 'y':
        nw = NodeWriter()
        nw.del_user(group, client_index)
    else:
        print("撤销删除")