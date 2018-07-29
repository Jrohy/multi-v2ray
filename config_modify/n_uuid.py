#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uuid
import read_json
import write_json
from base_util import tool_box

mul_user_conf = read_json.multiUserConf

length = len(mul_user_conf)

choice = 1

if length > 1:
    import server_info
    choice=input("请输入要改UUID的节点序号数字:")
    if not tool_box.is_number(choice):
        print("输入错误，请检查是否为数字")
        exit()
    choice = int(choice)

if length == 1 or (choice > 0 and choice <= len(mul_user_conf)):
    if mul_user_conf[choice - 1]["protocol"] == "vmess":
        print ("当前节点UUID为：%s" % mul_user_conf[choice - 1]['id'])
        if_gen_uuid=input("是否要随机生成一个新的UUID (y/n)：")
        if if_gen_uuid=="y":
            new_uuid = uuid.uuid1()
            print("新的UUID为：%s" % new_uuid)
            write_json.write_uuid(new_uuid, mul_user_conf[choice - 1]['indexDict'])
            print("UUID修改成功！")
        else:
            print("已取消生成新的UUID,未执行任何操作")
    else:
        print("只有vmess协议才能修改uuid!")
else:
    print ("输入错误，请检查是否符合范围中")