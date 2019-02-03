#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ..util_core.group import Vmess, Socks, Mtproto, SS
from ..util_core.writer import ClientWriter, GroupWriter
from ..util_core.selector import ClientSelector, GroupSelector

def alterid():
    cs = ClientSelector('修改alterId')
    group = cs.group

    if group == None:
        pass
    else:
        client_index = cs.client_index
        if type(group.node_list[client_index]) == Vmess:
            print("当前节点alterID: {}".format(group.node_list[client_index].alter_id))
            new_alterid = input("请输入新的alterID: ")
            if (new_alterid.isnumeric()):
                cw = ClientWriter(group.tag, group.index, client_index)
                cw.write_aid(int(new_alterid))
                print("alterID修改成功！")
            else:
                print ("输入错误，请检查是否为数字")
        else:
            print("只有vmess协议才能修改alterId!")

def dyn_port():
    gs = GroupSelector('修改动态端口')
    group = gs.group

    if group == None:
        pass
    else:
        print('当前组的动态端口状态：{}'.format(group.dyp))
        gw = GroupWriter(group.tag, group.index)
        
        choice = input("是否开启动态端口(y/n): ").lower()

        if choice == 'y':
            newAlterId = input("请为动态端口设置alterID(默认32): ")
            newAlterId = '32' if newAlterId == '' else newAlterId
            if (newAlterId.isdecimal()):
                gw.write_dyp(True, newAlterId)
                print("\n成功开启动态端口!")
            else:
                print ("\n输入错误，请检查是否为数字")
        elif choice == 'n':
            gw.write_dyp(False)
            print("\n成功关闭动态端口!")
        else:
            print ("\n输入错误，请检查重新输入")

def new_email():
    cs = ClientSelector('修改email')
    group = cs.group

    if group == None:
        pass
    elif type(group.node_list[0]) == Socks:
        print("Socks5节点 不支持写入email!")
    else:
        client_index = cs.client_index
        group_list = cs.group_list
        print ("当前节点email为：{}".format(group.node_list[client_index].user_info))
        email = ""
        while True:
            is_duplicate_email=False
            email = input("请输入新的email地址: ")
            if email == "":
                break
            from ..util_core.utils import is_email
            if not is_email(email):
                print("不是合格的email格式，请重新输入")
                continue
            
            for loop_group in group_list:
                for node in loop_group.node_list:
                    if node.user_info == None or node.user_info == '':
                        continue
                    elif node.user_info == email:
                        print("已经有重复的email, 请重新输入")
                        is_duplicate_email = True
                        break              
            if not is_duplicate_email:
                break

        if email != "":
            cw = ClientWriter(group.tag, group.index, client_index)
            cw.write_email(email)
            print("修改email成功!")

def new_uuid():
    cs = ClientSelector('修改uuid')
    group = cs.group

    if group == None:
        pass
    else:
        client_index = cs.client_index
        if type(group.node_list[client_index]) == Vmess:
            print("当前节点UUID为：{}".format(group.node_list[client_index].password))
            choice = input("是否要随机生成一个新的UUID (y/n)：").lower()
            if choice == "y":
                import uuid
                new_uuid = uuid.uuid1()
                print("新的UUID为：{}".format(new_uuid))
                cw = ClientWriter(group.tag, group.index, client_index)
                cw.write_uuid(new_uuid)
                print("UUID修改成功！")
            else:
                print("已取消生成新的UUID,未执行任何操作")
        else:
            print("只有vmess协议才能修改uuid!")

def port():
    gs = GroupSelector('修改port')
    group = gs.group

    if group == None:
        pass
    else:
        if group.end_port:
            port_info = "{0}-{1}".format(group.port, group.end_port)
        else:
            port_info = group.port
        print('当前组的端口信息为：{}'.format(port_info))
        new_port_info = input("请输入新端口(支持输入端口范围, 用'-'隔开, 表示该范围的全部端口生效)：")
        import re
        if new_port_info.isdecimal() or re.match(r'^\d+\-\d+$', new_port_info):
            gw = GroupWriter(group.tag, group.index)
            gw.write_port(new_port_info)
            print('端口修改成功！')
        else:
            print("输入错误!")

def tfo():
    gs = GroupSelector('修改tcpFastOpen')
    group = gs.group

    if group == None:
        exit(-1)
    else:
        if type(group.node_list[0]) == Mtproto or type(group.node_list[0]) == SS:
            print("\nv2ray MTProto/Shadowsocks协议不支持配置tcpFastOpen!!!\n")
            exit(-1)
        
        print('当前组的tcpFastOpen状态：{}'.format(group.tfo))
        print("")
        print("1.开启TFO(强制开启)")
        print("2.关闭TFO(强制关闭)")
        print("3.删除TFO(使用系统默认设置)")
        choice = input("请输入数字选择功能：")
        
        gw = GroupWriter(group.tag, group.index)
        if choice == "1":
            gw.write_tfo('on')
        elif choice == "2":
            gw.write_tfo('off')
        elif choice == "3":
            gw.write_tfo('del')
        else:
            print("输入错误，请重试！")