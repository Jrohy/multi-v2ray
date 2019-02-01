#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ..util_core.group import Vmess
from ..util_core.writer import ClientWriter
from ..util_core.selector import ClientSelector

cs = ClientSelector('修改alterId')
group = cs.group

if group == None:
    pass
else:
    client_index = cs.client_index
    if type(group.node_list[client_index]) == Vmess:
        print("当前节点alterID: {}".format(group.node_list[client_index].alter_id))
        new_alterid = input("请输入新的alterID: ")
        if (new_alterid.isnumeric()):
            cw = ClientWriter(group.tag, group.index, client_index)
            cw.write_aid(int(new_alterid))
            print("alterID修改成功！")
        else:
            print ("输入错误，请检查是否为数字")
    else:
        print("只有vmess协议才能修改alterId!")