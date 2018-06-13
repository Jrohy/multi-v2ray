#! /usr/bin/env python
# -*- coding: utf-8 -*-
import read_json
import write_json
import base_util.v2ray_util as util

mul_user_conf = read_json.multiUserConf
choice=input("请输入要改alterId的节点序号:")
if util.is_number(choice) and choice > 0 and choice <= len(mul_user_conf):
    new_alterid=input("请输入新的alterID: ")
    if (util.is_number(new_alterid)):
        write_json.write_alterid(new_alterid, mul_user_conf[choice - 1]['indexDict'])
    else:
        print ("输入错误，请检查是否为数字")
else:
    print ("输入错误，请检查是否为数字和范围中")
