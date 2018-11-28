#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import time
import os
import urllib.request

from config import Config
from group import SS, Socks, Vmess,Mtproto, Group, Dyport, Quic

class Stats:
    def __init__(self, status=False, door_port=0):
        self.status = status
        self.door_port = door_port

    def __str__(self):
        return "开启" if self.status else "关闭"

class Profile:
    def __init__(self):
        self.path = Config().get_path('config_path')
        self.group_list = []
        self.stats = None
        self.ban_bt = False
        self.user_number = 0
        self.modify_time = os.path.getmtime(self.path)
        self.read_json()

    def __str__(self):
        result = ""
        for group in self.group_list:
            result = "{}{}".format(result, group)
        result = result + "Tip: 同一Group的节点传输方式,端口配置,TLS等设置相同\n"
        return result

    def read_json(self):

        with open(self.path, 'r') as json_file:
            self.config = json.load(json_file)

        #读取配置文件大框架
        conf_inbounds = self.config["inbounds"]
        conf_rules = self.config["routing"]["rules"]

        stats = Stats()
        if "stats" in self.config:
            stats.status = True
            for inbound in conf_inbounds:
                if "protocol" in inbound and inbound["protocol"] == "dokodemo-door":
                    stats.door_port = inbound["port"]
                    break
        self.stats = stats

        for rule in conf_rules:
            if "protocol" in rule and "bittorrent" in rule["protocol"]:
                self.ban_bt = True

        #获取本机IP地址
        my_ip = urllib.request.urlopen('http://api.ipify.org').read()
        local_ip = bytes.decode(my_ip)

        group_ascii = 64  # before 'A' ascii code
        for index, json_part in enumerate(conf_inbounds):
            group = self.parse_group(json_part, index, local_ip)
            if group != None:
                group_ascii = group_ascii + 1
                group.tag = chr(group_ascii)
                self.group_list.append(group)
        
        del self.config

    def parse_group(self, part_json, group_index, local_ip):
        dyp, quic, end_port, header, tfo, tls, path, host, conf_ip = Dyport(), None, None, None, None, "", "", "", local_ip
        
        protocol = part_json["protocol"]

        if protocol == 'dokodemo-door' or (protocol == "vmess" and "streamSettings" not in part_json):
            return

        conf_settings = part_json["settings"]

        port_info = str(part_json["port"]).split("-", 2)

        if len(port_info) == 2:
            port, end_port = port_info
        else:
            port = port_info[0]

        if "detour" in conf_settings:
            dynamic_port_tag = conf_settings["detour"]["to"]
            for inbound in self.config["inbounds"]:
                if "tag" in inbound and inbound["tag"] == dynamic_port_tag:
                    dyp.aid = inbound["settings"]["default"]["alterId"]
                    dyp.status = True
                    break

        if protocol == "vmess" or protocol == "socks":
            conf_stream = part_json["streamSettings"]
            tls = conf_stream["security"]

            if "sockopt" in conf_stream and "tcpFastOpen" in conf_stream["sockopt"]:
                tfo = "开启" if conf_stream["sockopt"]["tcpFastOpen"] else "关闭"

            if conf_stream["httpSettings"]:
                path = conf_stream["httpSettings"]["path"]
            elif conf_stream["wsSettings"]:
                host = conf_stream["wsSettings"]["headers"]["Host"]
                path = conf_stream["wsSettings"]["path"]
            elif conf_stream["tcpSettings"]:
                host = conf_stream["tcpSettings"]["header"]["request"]["headers"]["Host"]

            if (tls == "tls"):
                conf_ip = Config().get_data('domain')

            if conf_stream["network"] == "kcp" and "header" in conf_stream["kcpSettings"]:
                header = conf_stream["kcpSettings"]["header"]["type"]
            
            if conf_stream["network"] == "quic" and conf_stream["quicSettings"]:
                quic_settings = conf_stream["quicSettings"]
                quic = Quic(quic_settings["security"], quic_settings["key"], quic_settings["header"]["type"])
        
        group = Group(conf_ip, port,  end_port=end_port, tls=tls, tfo=tfo, dyp=dyp, index=group_index)

        if protocol == "shadowsocks":
            self.user_number = self.user_number + 1
            email = conf_settings["email"] if 'email' in conf_settings else ''
            ss = SS(self.user_number, conf_settings["password"], conf_settings["method"], email)
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
            self.user_number = self.user_number + 1
            if "email" in client and client["email"]:
                email = client["email"]

            if protocol == "vmess":
                node = Vmess(client["id"], client["alterId"], conf_stream["network"], self.user_number, path=path, host=host, header=header, email=email, quic=quic)

            elif protocol == "socks":
                node = Socks(self.user_number, client["pass"], user_info=client["user"])

            elif protocol == "mtproto":
                node = Mtproto(self.user_number, client["secret"], user_info=email)
                
            if not group.protocol:
                group.protocol = node.__class__.__name__

            group.node_list.append(node)
        return group