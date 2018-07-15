#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import write_json
import random
from base_util import tool_box

random_port = random.randint(1000, 65535)
new_port=input("产生随机端口%d, 回车直接以该端口新建Group, 否则输入自定义端口: " % random_port)

if not new_port:
    new_port = random_port
    
if tool_box.is_number(new_port):
    print("新端口为: %d" % new_port)
    write_json.create_new_port(new_port)
else:
    print ("\n输入错误，请检查是否为数字")
