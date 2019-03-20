#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ..util_core.group import Vmess, Socks, Mtproto, SS
from ..util_core.writer import ClientWriter, GroupWriter
from ..util_core.selector import ClientSelector, GroupSelector

def alterid():
    cs = ClientSelector(_('modify alterId'))
    group = cs.group

    if group == None:
        pass
    else:
        client_index = cs.client_index
        if type(group.node_list[client_index]) == Vmess:
            print("{}: {}".format(_("node alterID"), group.node_list[client_index].alter_id))
            new_alterid = input(_("please input new alterId: "))
            if (new_alterid.isnumeric()):
                cw = ClientWriter(group.tag, group.index, client_index)
                cw.write_aid(int(new_alterid))
                print(_("alterId modify success!"))
            else:
                print(_("input error, please check is number"))
        else:
            print(_("only vmess protocol can modify alterId!"))

def dyn_port():
    gs = GroupSelector(_('modify dyn_port'))
    group = gs.group

    if group == None:
        pass
    else:
        print('{}: {}'.format(_("dyn_port status"), group.dyp))
        gw = GroupWriter(group.tag, group.index)
        
        choice = input(_("open/close dyn_port(y/n): ")).lower()

        if choice == 'y':
            newAlterId = input(_("please input dyn_port alterID(default 32): "))
            newAlterId = '32' if newAlterId == '' else newAlterId
            if (newAlterId.isdecimal()):
                gw.write_dyp(True, newAlterId)
                print(_("open dyn_port success!"))
            else:
                print(_("input error, please check is number"))
        elif choice == 'n':
            gw.write_dyp(False)
            print(_("close dyn_port success!"))
        else:
            print(_("input error, please input again"))

def new_email():
    cs = ClientSelector(_('modify email'))
    group = cs.group

    if group == None:
        pass
    elif type(group.node_list[0]) == Socks:
        print(_("Socks5 don't support email!"))
    else:
        client_index = cs.client_index
        group_list = cs.group_list
        print ("{}: {}".format(_("node email"), group.node_list[client_index].user_info))
        email = ""
        while True:
            is_duplicate_email=False
            email = input(_("please input new email: "))
            if email == "":
                break
            from ..util_core.utils import is_email
            if not is_email(email):
                print(_("not email, please input again"))
                continue
            
            for loop_group in group_list:
                for node in loop_group.node_list:
                    if node.user_info == None or node.user_info == '':
                        continue
                    elif node.user_info == email:
                        print(_("have same email, please input other"))
                        is_duplicate_email = True
                        break              
            if not is_duplicate_email:
                break

        if email != "":
            cw = ClientWriter(group.tag, group.index, client_index)
            cw.write_email(email)
            print(_("modify email success!!"))

def new_uuid():
    cs = ClientSelector(_('modify uuid'))
    group = cs.group

    if group == None:
        pass
    else:
        client_index = cs.client_index
        if type(group.node_list[client_index]) == Vmess:
            print("{}: {}".format(_("node UUID"), group.node_list[client_index].password))
            choice = input(_("get new UUID?(y/n): ")).lower()
            if choice == "y":
                import uuid
                new_uuid = uuid.uuid1()
                print("{}: {}".format(_("new UUID"),new_uuid))
                cw = ClientWriter(group.tag, group.index, client_index)
                cw.write_uuid(new_uuid)
                print(_("UUID modify success!"))
            else:
                print(_("undo modify"))
        else:
            print(_("only vmess protocol can modify uuid!"))

def port():
    gs = GroupSelector(_('modify port'))
    group = gs.group

    if group == None:
        pass
    else:
        if group.end_port:
            port_info = "{0}-{1}".format(group.port, group.end_port)
        else:
            port_info = group.port
        print('{}: {}'.format(_("group port"), port_info))
        new_port_info = input(_("please input new port(support range port(use '-' as separator), all range port can effect):"))
        import re
        if new_port_info.isdecimal() or re.match(r'^\d+\-\d+$', new_port_info):
            gw = GroupWriter(group.tag, group.index)
            gw.write_port(new_port_info)
            print(_('port modify success!'))
        else:
            print(_("input error!"))

def tfo():
    gs = GroupSelector(_('modify tcpFastOpen'))
    group = gs.group

    if group == None:
        exit(-1)
    else:
        if type(group.node_list[0]) == Mtproto or type(group.node_list[0]) == SS:
            print(_("V2ray MTProto/Shadowsocks don't support tcpFastOpen!!!"))
            print("")
            exit(-1)
        
        print('{}: {}'.format(_("group tcpFastOpen"), group.tfo))
        print("")
        print(_("1.open TFO(force open)"))
        print(_("2.close TFO(force close)"))
        print(_("3.delete TFO(use system default profile)"))
        choice = input(_("please select: "))
        
        gw = GroupWriter(group.tag, group.index)
        if choice == "1":
            gw.write_tfo('on')
        elif choice == "2":
            gw.write_tfo('off')
        elif choice == "3":
            gw.write_tfo('del')
        else:
            print(_("input error, please input again"))