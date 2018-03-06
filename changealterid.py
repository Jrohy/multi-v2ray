#! /usr/bin/env python
# -*- coding: utf-8 -*-
import readjson
import writejson
import v2rayutil

#主要程序部分
print ("当前AlterId为：%d") % str(readjson.ConfAlterId)
print ("请输入新AlterId：")
newAlterId=raw_input()
if (v2rayutil.is_number(newAlterId)):
    writejson.WriteAlterID(newAlterId)
else:
    print ("输入错误，请检查是否为数字")
