#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import readjson
import writejson

rules = readjson.ConfRouting[u"settings"][u"rules"]

if rules[1][u"outboundTag"] == "direct":
    if_open_ad_function = "广告拦截功能： 未开启"
else:
    if_open_ad_function = "广告拦截功能： 开启"

print("")
print(if_open_ad_function)

print("")
print("1. 开启")
print("2. 关闭")

choice = raw_input("请选择： ")

if choice == "1":
    writejson.WriteAD("on")
elif choice == "2":
    writejson.WriteAD("off")
