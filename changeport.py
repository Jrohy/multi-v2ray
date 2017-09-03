#! /usr/bin/env python
# -*- coding: utf-8 -*-
import readjson
import writejson

#判断是否为数字的函数
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

#主要程序部分
print ("当前主端口为：%s") % str(readjson.ConfPort)
print ("请输入新端口：")
newport=raw_input()
if (is_number(newport)):
    writejson.WritePort(newport)
else:
    print ("输入错误，请检查是否为数字")
