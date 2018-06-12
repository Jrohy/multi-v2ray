#! /usr/bin/env python
# -*- coding: utf-8 -*-
import read_json
import write_json
import v2rayutil

#主要程序部分
print ("当前主端口为：%s") % str(read_json.ConfPort)
print ("请输入新端口：")
newport=raw_input()
if (v2rayutil.is_number(newport)):
    write_json.WritePort(newport)
else:
    print ("输入错误，请检查是否为数字")
