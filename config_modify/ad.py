#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from loader import Loader
from writer import GlobalWriter

loader = Loader()
profile = loader.profile
group_list = loader.profile.group_list
gw = GlobalWriter(group_list)

ad_status = "开启" if profile.ad else "关闭"
print("当前广告拦截功能状态: {}".format(ad_status))

print("")
print("1. 开启")
print("2. 关闭")

choice = input("请选择： ")

if choice == "1":
    gw.write_ad(True)
elif choice == "2":
    gw.write_ad(False)
else:
    print("输入有误!")