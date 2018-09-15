#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import read_json
import write_json
import re
from base_util import v2ray_util

mul_user_conf = read_json.multiUserConf

length = len(mul_user_conf)

choice = 'A'

if length > 1:
    import server_info
    choice=input("请输入要改tcpFastOpen的节点Group字母:")
    choice=choice.upper()

if length == 1 or (len(choice)==1 and re.match(r'[A-Z]', choice) and choice <= mul_user_conf[-1]['indexDict']['group']):
    for sin_user_conf in mul_user_conf:
        if sin_user_conf['indexDict']['group'] == choice:
            index_dict = sin_user_conf['indexDict']
            if sin_user_conf["protocol"] == "mtproto" or sin_user_conf["protocol"] == "shadowsocks":
                print("\nv2ray MTProto/Shadowsocks协议不支持配置tcpFastOpen!!!\n")
                exit()
            break

    tfo_status = sin_user_conf["tcpFastOpen"] if sin_user_conf["tcpFastOpen"] else "未设置"
    
    print("当前选择组tcpFastOpen状态：{}".format(tfo_status))
    print("")
    print("1.开启TFO(强制开启)")
    print("2.关闭TFO(强制关闭)")
    print("3.删除TFO(使用系统默认设置)")

    choice = input("请输入数字选择功能：")
    if choice == "1":
        write_json.write_tfo("on", index_dict)
    elif choice == "2":
        write_json.write_tfo("off", index_dict)
    elif choice == "3":
        write_json.write_tfo("del", index_dict)
    else:
        print("输入错误，请重试！")
else:
    print ("输入错误，请检查是否符合范围中")