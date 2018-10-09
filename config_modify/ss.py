#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import string
import sys

from group import SS
from writer import GroupWriter
from selector import GroupSelector

class SSFactory:
    def __init__(self):
        self.method_tuple = ("aes-256-cfb", "aes-128-cfb", "chacha20", 
        "chacha20-ietf", "aes-256-gcm", "aes-128-gcm", "chacha20-poly1305")

    def get_method(self):
        print ("请选择shadowsocks的加密方式：")
        for index, method in enumerate(self.method_tuple):
            print ("{}.{}".format(index + 1, method))
        choice = input()
        choice = int(choice)
        if choice < 0 or choice > len(self.method_tuple):
            print("输入错误，请检查是否符合范围中")
            exit(-1)
        else:
            return self.method_tuple[choice - 1]

    def get_password(self):
        random_pass = ''.join(random.sample(string.ascii_letters + string.digits, 16))
        new_pass =input("产生随机密码 {} , 回车直接使用该密码, 否则输入自定义密码: ".format(random_pass))
        if not new_pass:
            new_pass = random_pass
        return new_pass

if __name__ == '__main__':

    # 外部传参来决定修改哪种, 默认修改method
    choice = "method"
    correct_way = ("method", "password")

    if len(sys.argv) > 1:
        choice = sys.argv[1]
        if choice not in correct_way:
            print("传参有误!")
            exit(-1)
    else:
        print("请传以下参数来修改ss配置: {}". format(correct_way))
        exit(-1)

    gs = GroupSelector('修改SS')
    group = gs.group

    if group == None:
        exit(-1)
    elif type(group.node_list[0]) != SS:
        print("\n当前选择组不是Shadowsocks协议!\n")
        exit(-1)
    else:
        sm = SSFactory()
        gw = GroupWriter(group.tag, group.index)
        if choice == correct_way[0]:
            gw.write_ss_method(sm.get_method())
        elif choice == correct_way[1]:
            gw.write_ss_password(sm.get_password())
        print("修改Shadowsocks {}成功!\n".format(choice))