#! /usr/bin/env python
# -*- coding: utf-8 -*-

import read_json
import base64
import json

if len(read_json.multiUserConf) > 1 or __name__== "__main__":
    for index, sin_user_conf in enumerate(read_json.multiUserConf):
        index += 1
        print("%d." % index)
        print("Group: %s" % sin_user_conf["indexDict"]["group"])
        print("IP：%s" % str(sin_user_conf["add"])) 
        print("Port：%s" % str(sin_user_conf["port"])) 
        print("UUID：%s" % str(sin_user_conf["id"])) 
        print("Alter ID: %s" % str(sin_user_conf["aid"])) 
        print("Network：%s" % str(sin_user_conf["net"] + " " + sin_user_conf["type"])) 
        print("TLS: %s" % str("关闭" if sin_user_conf["tls"] == "" else "开启"))
        print("DynamicPort: %s" % read_json.conf_Dyp)

        sin_user_conf.pop('indexDict')
        base64_str = base64.b64encode(bytes(json.dumps(sin_user_conf), 'utf-8'))

        #绿色字体显示
        print("\033[32m")
        print("vmess://%s" % bytes.decode(base64_str))
        print("\033[0m")
        print("")

    print("Tip: 同一Group的节点除了uuid和alterid独立外，其他信息都一致\n")