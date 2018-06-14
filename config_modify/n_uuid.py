#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uuid
import read_json
import write_json
from base_util import v2ray_util

mul_user_conf = read_json.multiUserConf

choice=input("请输入要改UUID的节点序号:")
if not v2ray_util.is_number(choice):
    print("输入错误，请检查是否为数字")
    exit
choice = int(choice)

if choice > 0 and choice <= len(mul_user_conf):
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
    print ("输入错误，请检查是否符合范围中")