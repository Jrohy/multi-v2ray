#! /usr/bin/env python
# -*- coding: utf-8 -*-
import read_json
import write_json
from base_util import v2ray_util

mul_user_conf = read_json.multiUserConf
choice=input("请输入要改tls的节点序号:")
if v2ray_util.is_number(choice) and choice > 0 and choice <= len(mul_user_conf):
    if (mul_user_conf[choice - 1]['port']=="tls"):
        mystreamsecurity="TLS：开启"
    else:
        mystreamsecurity="TLS：关闭"

    index_dict = mul_user_conf[choice - 1]['indexDict']
    print("当前选择节点状态：\n" + mystreamsecurity)
    print("")
    print("1.开启TLS")
    print("2.关闭TLS")

    choice = input("请输入数字选择功能：")
    if choice == "1":
        v2ray_util.change_tls("on", index_dict)
    elif choice == "2":
        v2ray_util.change_tls("off", index_dict)
    else:
        print("输入错误，请重试！")
else:
    print ("输入错误，请检查是否为数字和范围中")
