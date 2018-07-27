#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import read_json
import base64
import json

for index, sin_user_conf in enumerate(read_json.multiUserConf):
    index += 1
    protocol=sin_user_conf["protocol"]
    print("%d." % index)
    print("Group: %s" % sin_user_conf["indexDict"]["group"])
    print("IP：%s" % sin_user_conf["add"]) 
    print("Port：%s" % sin_user_conf["port"])
    if sin_user_conf["email"]:
        if protocol == "vmess" or protocol == "mtproto":
            print("Email: %s" % sin_user_conf["email"])
        elif protocol == "socks":
            print("User: %s" % sin_user_conf["email"])
    if protocol == "vmess":
        print("UUID：%s" % sin_user_conf["id"])
        print("Alter ID: %s" % sin_user_conf["aid"])
        if sin_user_conf["net"] == "h2":
            print("Network：%s" % ("HTTP/2  伪装Path: " + sin_user_conf["path"])) 
        elif sin_user_conf["net"] == "ws":
            print("Network：%s" % ("WebSocket  伪装Host: " + sin_user_conf["host"] + " 伪装Path: " + sin_user_conf["path"])) 
        else:
            print("Network：%s" % (sin_user_conf["net"] + " " + sin_user_conf["type"])) 
        print("TLS: %s" % ("关闭" if sin_user_conf["tls"] == "" else "开启"))
        print("DynamicPort: %s" % sin_user_conf["dyp"])

        copy_conf = sin_user_conf.copy()
        copy_conf.pop('indexDict')
        copy_conf.pop('dyp')
        copy_conf.pop('email')
        copy_conf.pop('protocol')
        base64_str = base64.b64encode(bytes(json.dumps(copy_conf), 'utf-8'))

        share_url = "vmess://" + bytes.decode(base64_str)
        
    elif protocol == "socks":
        print("Pass: %s" % sin_user_conf["id"])
        print("UDP: true")
        print("TLS: %s" % ("关闭" if sin_user_conf["tls"] == "" else "开启"))
        if sin_user_conf["tls"] == "":
            share_url = "tg://socks?server=%s&port=%s&user=%s&pass=%s" % (sin_user_conf["add"], sin_user_conf["port"], sin_user_conf["email"], sin_user_conf["id"])
        else:
            share_url = "HTTPS的Socks5不支持tg的分享连接. 请自行配合设置BifrostV等软件使用"

    elif protocol == "mtproto":
        print("Secret: %s" % sin_user_conf["id"])
        share_url = "tg://proxy?server=%s&port=%s&secret=%s" % (sin_user_conf["add"], sin_user_conf["port"], sin_user_conf["id"])

    #绿色字体显示
    print("\033[32m")
    print(share_url)
    print("\033[0m")
    print("")

print("Tip: 同一Group的节点传输方式,端口,TLS,动态端口等设置相同\n")