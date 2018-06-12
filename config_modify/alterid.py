#! /usr/bin/env python
# -*- coding: utf-8 -*-
import read_json
import write_json
from base_util import v2ray_util

new_alterid=input("请输入新的alterID: ")
if (v2ray_util.is_number(new_alterid)):
    write_json.write_alterid(new_alterid)
else:
    print ("输入错误，请检查是否为数字")
