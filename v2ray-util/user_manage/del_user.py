#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from ..writer import NodeWriter
from ..selector import ClientSelector
from ..utils import clean_iptables

cs = ClientSelector('删除user')
group = cs.group

if group == None:
    pass
else:
    client_index = cs.client_index
    print("你选择的user信息:")
    print(group.show_node(client_index))
    choice = input("是否删除y/n：").lower()
    if choice == 'y':
        if len(group.node_list) == 1:
            clean_iptables(group.port)
        nw = NodeWriter()
        nw.del_user(group, client_index)
    else:
        print("撤销删除")