#! /usr/bin/env python
# -*- coding: utf-8 -*-
import write_json
from base_util import v2ray_util

new_port=input("请输入新端口：")
if v2ray_util.is_number(new_port):
    write_json.create_new_port(new_port)
else:
    print ("\n输入错误，请检查是否为数字")
