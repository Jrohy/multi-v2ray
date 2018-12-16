#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
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
        # 自动清理没用的iptables规则
        os.system("bash /usr/local/multi-v2ray/global_setting/clean_iptables.sh")
    else:
        print("撤销删除")