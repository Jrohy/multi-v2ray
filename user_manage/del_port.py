#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from writer import NodeWriter
from selector import GroupSelector

gs = GroupSelector('删除port')
group = gs.group

if group == None:
    exit(-1)
else:
    print("你要删除的Group组所有节点信息: ")
    print(group)
    choice = input("是否删除y/n：").lower()
    if choice == 'y':
        nw = NodeWriter()
        nw.del_port(group)
    else:
        print("撤销删除")