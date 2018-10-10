#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import time
import os
import urllib.request

from group import Dyport, SS, Socks, Vmess,Mtproto, Group

conf_inboundDetour = ""

local_ip = ""

user_number = 0

def parse_dyp(conf_settings):
    dyp = Dyport()
    if "detour" in conf_settings:
        dynamic_port_tag = conf_settings["detour"]["to"]
        for detour_list in conf_inboundDetour:
            if "tag" in detour_list and detour_list["tag"] == dynamic_port_tag:
                dyp.aid = detour_list["settings"]["default"]["alterId"]
                dyp.status = True
                break
    return dyp

def parse_group(part_json, group_index):
    header, tfo, tls, path, host, conf_ip = None, None, "", "", "", local_ip

    global user_number
    
    protocol = part_json["protocol"]

    if protocol == 'dokodemo-door' or 'allocate' in part_json:
        return

    conf_settings = part_json["settings"]

    dyp = parse_dyp(conf_settings)

    if protocol == "vmess" or protocol == "socks":
        conf_stream = part_json["streamSettings"]
        tls = conf_stream["security"]

        if "sockopt" in conf_stream and "tcpFastOpen" in conf_stream["sockopt"]:
           tfo = "开启" if conf_stream["sockopt"]["tcpFastOpen"] else "关闭"

        if conf_stream["httpSettings"] != None:
            path = conf_stream["httpSettings"]["path"]
        elif conf_stream["wsSettings"] != None:
            host = conf_stream["wsSettings"]["headers"]["Host"]
            path = conf_stream["wsSettings"]["path"]
        elif conf_stream["tcpSettings"] != None:
            host = conf_stream["tcpSettings"]["header"]["request"]["headers"]["Host"]

        if (tls == "tls"):
            with open('/usr/local/multi-v2ray/my_domain', 'r') as domain_file:
                conf_ip = str(domain_file.read())

        if conf_stream["network"] == "kcp" and "header" in conf_stream["kcpSettings"]:
            header = conf_stream["kcpSettings"]["header"]["type"]
    
    group = Group(conf_ip, part_json["port"], tls=tls, tfo=tfo, dyp=dyp, index=group_index)

    if protocol == "shadowsocks":
        user_number = user_number + 1
        email = conf_settings["email"] if 'email' in conf_settings else ''
        ss = SS(user_number, conf_settings["password"], conf_settings["method"], email)
        group.node_list.append(ss)
        group.protocol = ss.__class__.__name__
        return group
    elif protocol == "vmess":
        clients=conf_settings["clients"]
    elif protocol == "socks":
        clients=conf_settings["accounts"]
    elif protocol == "mtproto":
        clients=conf_settings["users"]

    for client in clients:
        email, node = "", None
        user_number = user_number + 1
        if "email" in client and client["email"] != None:
            email = client["email"]

        if protocol == "vmess":
            node = Vmess(client["id"], client["alterId"], conf_stream["network"], user_number, path=path, host=host, header=header, email=email)

        elif protocol == "socks":
            node = Socks(user_number, client["pass"], user_info=client["user"])

        elif protocol == "mtproto":
            node = Mtproto(user_number, client["secret"], user_info=email)
            
        if not group.protocol:
            group.protocol = node.__class__.__name__

        group.node_list.append(node)
    return group

class Stats:
    def __init__(self, status=False, door_port=0):
        self.status = status
        self.door_port = door_port

    def __str__(self):
        return "开启" if self.status else "关闭"

class Profile:
    def __init__(self, path='/etc/v2ray/config.json'):
        self.path = path
        self.ad = None
        self.group_list = []
        self.stats = None
        self.modify_time = os.path.getmtime(path)
        self.read_json()

    def __str__(self):
        result = ""
        for group in self.group_list:
            result = "{}{}".format(result, group)
        result = result + "Tip: 同一Group的节点传输方式,端口,TLS,动态端口等设置相同\n"
        return result

    def read_json(self):
        global local_ip
        global conf_inboundDetour

        with open(self.path, 'r') as json_file:
            config = json.load(json_file)

        #读取配置文件大框架
        conf_inbound = config["inbound"]
        conf_inboundDetour = config["inboundDetour"]
        conf_routing = config["routing"]

        self.ad = True if conf_routing["settings"]["rules"][0]["outboundTag"] == "blocked" else False

        stats = Stats()
        if "stats" in config:
            stats.status = True
            for detour_list in conf_inboundDetour:
                if "protocol" in detour_list and detour_list["protocol"] == "dokodemo-door":
                    stats.door_port = detour_list["port"]
        
        self.stats = stats

        #获取本机IP地址
        my_ip = urllib.request.urlopen('http://api.ipify.org').read()
        local_ip = bytes.decode(my_ip)

        json_part_list = [conf_inbound]
        if conf_inboundDetour:
            json_part_list.extend([x for x in conf_inboundDetour])

        group_ascii = 64  # before 'A' ascii code
        for index, json_part in enumerate(json_part_list):
            group = parse_group(json_part, index - 1)
            if group != None:
                group_ascii = group_ascii + 1
                group.tag = chr(group_ascii)
                self.group_list.append(group)