#! /usr/bin/env python
# -*- coding: utf-8 -*-
import readjson
import writejson
import v2rayutil

#主要程序部分
print ("当前主端口为：%s") % str(readjson.ConfPort)
print ("请输入新端口：")
newport=raw_input()
if (v2rayutil.is_number(newport)):
    writejson.WritePort(newport)
else:
    print ("输入错误，请检查是否为数字")
