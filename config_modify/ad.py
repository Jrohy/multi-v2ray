#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import read_json
import write_json

rules = read_json.conf_routing[u"settings"][u"rules"]

if rules[0][u"outboundTag"] == "direct":
    if_open_ad_function = "广告拦截功能： 未开启"
else:
    if_open_ad_function = "广告拦截功能： 开启"

print("")
print(if_open_ad_function)

print("")
print("1. 开启")
print("2. 关闭")

choice = input("请选择： ")

if choice == "1":
    write_json.write_ad("on")
elif choice == "2":
    write_json.write_ad("off")
