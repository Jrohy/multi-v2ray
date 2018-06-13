#! /usr/bin/env python
# -*- coding: utf-8 -*-
import write_json
import base_util.v2ray_util as util

new_port=input("请输入新端口：")
if util.is_number(new_port):
    write_json.create_new_port(new_port)
else:
    print ("\n输入错误，请检查是否为数字")
