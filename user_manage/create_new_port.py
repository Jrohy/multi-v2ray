#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import write_json
from base_util import tool_box

new_port=input("请输入新端口：")
if tool_box.is_number(new_port):
    write_json.create_new_port(new_port)
else:
    print ("\n输入错误，请检查是否为数字")
