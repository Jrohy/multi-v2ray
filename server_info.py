#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import read_json
import base64
import json

for index, sin_user_conf in enumerate(read_json.multiUserConf):
    index += 1
    print("%d." % index)
    print("Group: %s" % sin_user_conf["indexDict"]["group"])
    print("IP：%s" % str(sin_user_conf["add"])) 
    print("Port：%s" % str(sin_user_conf["port"])) 
    print("UUID：%s" % str(sin_user_conf["id"])) 
    print("Alter ID: %s" % str(sin_user_conf["aid"]))
    if sin_user_conf["net"] == "h2":
        print("Network：%s" % str("HTTP/2  伪装Path: " + sin_user_conf["path"])) 
    else:
        print("Network：%s" % str(sin_user_conf["net"] + " " + sin_user_conf["type"])) 
    print("TLS: %s" % str("关闭" if sin_user_conf["tls"] == "" else "开启"))
    print("DynamicPort: %s" % sin_user_conf["dyp"])

    copy_conf = sin_user_conf.copy()
    copy_conf.pop('indexDict')
    copy_conf.pop('dyp')
    base64_str = base64.b64encode(bytes(json.dumps(copy_conf), 'utf-8'))

    #绿色字体显示
    print("\033[32m")
    print("vmess://%s" % bytes.decode(base64_str))
    print("\033[0m")
    print("")

print("Tip: 同一Group的节点传输方式,端口,TLS,动态端口等设置相同\n")