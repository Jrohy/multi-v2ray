#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os

from v2ray_util import run_type
from .config import Config
from .utils import ColorStr, get_ip
from .group import SS, Socks, Vmess, Vless, Mtproto, Quic, Group, Dyport, Trojan

class Stats:
    def __init__(self, status=False, door_port=0):
        self.status = status
        self.door_port = door_port

    def __str__(self):
        return "open" if self.status else "close"

class Profile:
    def __init__(self):
        self.path = Config().get_path('config_path')
        self.group_list = []
        self.stats = None
        self.ban_bt = False
        self.user_number = 0
        self.network = "ipv4"
        self.modify_time = os.path.getmtime(self.path)
        self.read_json()

    def __str__(self):
        result = ""
        for group in self.group_list:
            result = "{}{}".format(result, group)
        result = result + _("Tip: The same group's node protocol, port, tls are the same.")
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

        local_ip = get_ip()

        if ":" in local_ip:
            self.network = "ipv6"

        group_ascii = 64  # before 'A' ascii code
        for index, json_part in enumerate(conf_inbounds):
            group = self.parse_group(json_part, index, local_ip)
            if group != None:
                group_ascii = group_ascii + 1
                if group_ascii > 90:
                    group.tag = str(group_ascii)
                else:
                    group.tag = chr(group_ascii)
                self.group_list.append(group)
        
        if len(self.group_list) == 0:
            print("{} json no streamSettings item, please run {} to recreate {} json!".format(run_type, ColorStr.cyan("{} new".format(run_type)), run_type))

        del self.config

    def parse_group(self, part_json, group_index, local_ip):
        dyp, quic, end_port, tfo, header, tls, path, host, conf_ip, serviceName, mode, serverName, privateKey, shortId = Dyport(), None, None, None, "", "", "", "", local_ip, "", "gun", "", "", ""
        
        protocol = part_json["protocol"]

        if protocol == 'dokodemo-door' or (protocol == "vmess" and "streamSettings" not in part_json):
            return

        conf_settings = part_json["settings"]

        port_info = str(part_json["port"]).split("-", 2)

        if "domain" in part_json and part_json["domain"]:
            conf_ip = part_json["domain"]

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

        if protocol in ("vmess", "vless", "socks", "trojan"):
            conf_stream = part_json["streamSettings"]
            tls = conf_stream["security"]

            if tls == "reality" and conf_stream["realitySettings"]:
                serverName = conf_stream["realitySettings"]["serverNames"][0]
                privateKey = conf_stream["realitySettings"]["privateKey"]
                shortId = conf_stream["realitySettings"]["shortIds"][0]

            if "sockopt" in conf_stream and "tcpFastOpen" in conf_stream["sockopt"]:
                tfo = "open" if conf_stream["sockopt"]["tcpFastOpen"] else "close"

            if "httpSettings" in conf_stream and conf_stream["httpSettings"]:
                path = conf_stream["httpSettings"]["path"]
            elif "wsSettings" in conf_stream and conf_stream["wsSettings"]:
                host = conf_stream["wsSettings"]["headers"]["Host"]
                path = conf_stream["wsSettings"]["path"]
            elif "tcpSettings" in conf_stream and conf_stream["tcpSettings"]:
                host = conf_stream["tcpSettings"]["header"]["request"]["headers"]["Host"]
                header = "http"

            if conf_stream["network"] == "kcp" and "header" in conf_stream["kcpSettings"]:
                header = conf_stream["kcpSettings"]["header"]["type"]
                if "seed" in conf_stream["kcpSettings"]:
                    path = conf_stream["kcpSettings"]["seed"]
            
            if conf_stream["network"] == "quic" and conf_stream["quicSettings"]:
                quic_settings = conf_stream["quicSettings"]
                quic = Quic(quic_settings["security"], quic_settings["key"], quic_settings["header"]["type"])
            if conf_stream["network"] == "grpc" and conf_stream["grpcSettings"]:
                serviceName = conf_stream["grpcSettings"]["serviceName"]
                if "multiMode" in conf_stream["grpcSettings"] and conf_stream["grpcSettings"]["multiMode"]:
                    mode = "multi"
        
        group = Group(conf_ip, port,  end_port=end_port, tls=tls, tfo=tfo, dyp=dyp, index=group_index)

        if protocol == "shadowsocks":
            self.user_number = self.user_number + 1
            email = conf_settings["email"] if 'email' in conf_settings else ''
            ss = SS(self.user_number, conf_settings["password"], conf_settings["method"], email)
            group.node_list.append(ss)
            group.protocol = ss.__class__.__name__
            return group
        elif protocol in ("vmess", "vless", "trojan"):
            clients=conf_settings["clients"]
        elif protocol == "socks":
            clients=conf_settings["accounts"]
        elif protocol == "mtproto":
            clients=conf_settings["users"]

        for client in clients:
            email, node, flow = "", None, ""
            self.user_number = self.user_number + 1
            if "email" in client and client["email"]:
                email = client["email"]

            if protocol == "vmess":
                if serviceName:
                    path = serviceName
                    header = mode
                node = Vmess(client["id"], client["alterId"], conf_stream["network"], self.user_number, path=path, host=host, header=header, email=email, quic=quic)

            elif protocol == "socks":
                node = Socks(self.user_number, client["pass"], user_info=client["user"])

            elif protocol == "mtproto":
                node = Mtproto(self.user_number, client["secret"], user_info=email)

            elif protocol == "vless":
                if "flow" in client:
                    flow = client["flow"]
                node = Vless(client["id"], self.user_number, conf_settings["decryption"], email, conf_stream["network"], path, host, header, flow, serviceName, mode, serverName, privateKey, shortId)

            elif protocol == "trojan":
                node = Trojan(self.user_number, client["password"], email)
                
            if not group.protocol:
                group.protocol = node.__class__.__name__

            group.node_list.append(node)
        return group