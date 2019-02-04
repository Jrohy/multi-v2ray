#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ..util_core.group import Vmess, Socks, Mtproto, SS
from ..util_core.writer import ClientWriter, GroupWriter
from ..util_core.selector import ClientSelector, GroupSelector

def alterid():
    cs = ClientSelector('modify alterId')
    group = cs.group

    if group == None:
        pass
    else:
        client_index = cs.client_index
        if type(group.node_list[client_index]) == Vmess:
            print("node alterID: {}".format(group.node_list[client_index].alter_id))
            new_alterid = input("please input new alterID: ")
            if (new_alterid.isnumeric()):
                cw = ClientWriter(group.tag, group.index, client_index)
                cw.write_aid(int(new_alterid))
                print("alterID modify success！")
            else:
                print ("input error, please check is number")
        else:
            print("only vmess protocol can modify alterId!")

def dyn_port():
    gs = GroupSelector('modify dyn_port')
    group = gs.group

    if group == None:
        pass
    else:
        print('dyn_port status：{}'.format(group.dyp))
        gw = GroupWriter(group.tag, group.index)
        
        choice = input("open/close dyn_port(y/n): ").lower()

        if choice == 'y':
            newAlterId = input("please input dyn_port alterID(default 32): ")
            newAlterId = '32' if newAlterId == '' else newAlterId
            if (newAlterId.isdecimal()):
                gw.write_dyp(True, newAlterId)
                print("\nopen dyn_port success!")
            else:
                print ("\ninput error, please check is number")
        elif choice == 'n':
            gw.write_dyp(False)
            print("\nclose dyn_port success!")
        else:
            print ("\ninput error, please try again")

def new_email():
    cs = ClientSelector('modify email')
    group = cs.group

    if group == None:
        pass
    elif type(group.node_list[0]) == Socks:
        print("Socks5 don't support email!")
    else:
        client_index = cs.client_index
        group_list = cs.group_list
        print ("node email：{}".format(group.node_list[client_index].user_info))
        email = ""
        while True:
            is_duplicate_email=False
            email = input("please input new email: ")
            if email == "":
                break
            from ..util_core.utils import is_email
            if not is_email(email):
                print("not email, please input again")
                continue
            
            for loop_group in group_list:
                for node in loop_group.node_list:
                    if node.user_info == None or node.user_info == '':
                        continue
                    elif node.user_info == email:
                        print("have same email, please input other")
                        is_duplicate_email = True
                        break              
            if not is_duplicate_email:
                break

        if email != "":
            cw = ClientWriter(group.tag, group.index, client_index)
            cw.write_email(email)
            print("modify email success!")

def new_uuid():
    cs = ClientSelector('modify uuid')
    group = cs.group

    if group == None:
        pass
    else:
        client_index = cs.client_index
        if type(group.node_list[client_index]) == Vmess:
            print("node UUID：{}".format(group.node_list[client_index].password))
            choice = input("get new UUID?(y/n)：").lower()
            if choice == "y":
                import uuid
                new_uuid = uuid.uuid1()
                print("new UUID: {}".format(new_uuid))
                cw = ClientWriter(group.tag, group.index, client_index)
                cw.write_uuid(new_uuid)
                print("UUID modify success！")
            else:
                print("undo modify")
        else:
            print("only vmess protocol can modify uuid!")

def port():
    gs = GroupSelector('modify port')
    group = gs.group

    if group == None:
        pass
    else:
        if group.end_port:
            port_info = "{0}-{1}".format(group.port, group.end_port)
        else:
            port_info = group.port
        print('group port：{}'.format(port_info))
        new_port_info = input("please input new port(support range port(use '-' as separator), all range port can effect)：")
        import re
        if new_port_info.isdecimal() or re.match(r'^\d+\-\d+$', new_port_info):
            gw = GroupWriter(group.tag, group.index)
            gw.write_port(new_port_info)
            print('port modify success！')
        else:
            print("input error!")

def tfo():
    gs = GroupSelector('modify tcpFastOpen')
    group = gs.group

    if group == None:
        exit(-1)
    else:
        if type(group.node_list[0]) == Mtproto or type(group.node_list[0]) == SS:
            print("\nv2ray MTProto/Shadowsocks don't support tcpFastOpen!!!\n")
            exit(-1)
        
        print('group tcpFastOpen：{}'.format(group.tfo))
        print("")
        print("1.open TFO(force open)")
        print("2.close TFO(force close)")
        print("3.delete TFO(use system default profile)")
        choice = input("please select：")
        
        gw = GroupWriter(group.tag, group.index)
        if choice == "1":
            gw.write_tfo('on')
        elif choice == "2":
            gw.write_tfo('off')
        elif choice == "3":
            gw.write_tfo('del')
        else:
            print("input error, please try again!")