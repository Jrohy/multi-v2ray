#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uuid

from group import Vmess
from writer import ClientWriter
from selector import ClientSelector

cs = ClientSelector('修改uuid')
client_index = cs.client_index
group = cs.group

if group == None:
    exit(-1)
else:
    if type(group.node_list[client_index]) == Vmess:
        print("当前节点UUID为：{}".format(group.node_list[client_index].password))
        choice = input("是否要随机生成一个新的UUID (y/n)：").lower()
        if choice == "y":
            new_uuid = uuid.uuid1()
            print("新的UUID为：{}".format(new_uuid))
            cw = ClientWriter(group.tag, group.index, client_index)
            cw.write_uuid(new_uuid)
            print("UUID修改成功！")
        else:
            print("已取消生成新的UUID,未执行任何操作")
    else:
        print("只有vmess协议才能修改uuid!")