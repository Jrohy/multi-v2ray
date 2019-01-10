#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from ..writer import GroupWriter
from ..selector import GroupSelector

gs = GroupSelector('修改port')
group = gs.group

if group == None:
    pass
else:
    if group.end_port:
        port_info = "{0}-{1}".format(group.port, group.end_port)
    else:
        port_info = group.port
    print('当前组的端口信息为：{}'.format(port_info))

    port_strategy="always"
    new_port_info = input("请输入新端口(支持输入端口范围, 用'-'隔开, 表示该范围的全部端口生效)：")
    if new_port_info.isdecimal() or re.match(r'^\d+\-\d+$', new_port_info):
        gw = GroupWriter(group.tag, group.index)
        gw.write_port(new_port_info)
        print('端口修改成功！')
    else:
        print("输入错误!")