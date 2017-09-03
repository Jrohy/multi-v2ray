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
print ("当前加密方式为：%s") % str(readjson.ConfSecurity)
print ("请选择新的加密方式：")
print ("1.aes-128-cfb")
print ("2.aes-128-gcm")
print ("3.chacha20-poly1305")
print ("4.none")
newsecurity=raw_input()

if ( not is_number(newsecurity)):
    print ("输入错误，请检查输入是否为数字")
    exit
else:
    if (newsecurity=="1"):
        writejson.WriteSecurity("aes-128-cfb")
    elif(newsecurity=="2"):
        writejson.WriteSecurity("aes-128-gcm")
    elif(newsecurity=="3"):
        writejson.WriteSecurity("chacha20-poly1305")
    elif(newsecurity=="4"):
        writejson.WriteSecurity("none")
    else:
        print("请输入1-4之间的数字！")