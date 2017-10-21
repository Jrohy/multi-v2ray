#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import readjson
import urllib2

#写客户端配置文件函数
def WriteClientJson():
    myjsondump=json.dumps(clientconfig,indent=1)
    openjsonfile=file("/root/config.json","w+")
    openjsonfile.writelines(myjsondump)
    openjsonfile.close()

#获取本机IP地址
myip = urllib2.urlopen('http://api.ipify.org').read()
myip = myip.strip()

#加载客户端配置模板
clientjsonfile = file("/usr/local/v2ray.fun/json_template/client.json")
clientconfig = json.load(clientjsonfile)

#使用服务端配置来修改客户端模板
clientconfig[u"outbound"][u"settings"][u"vnext"][0][u"port"]=int(readjson.ConfPort)
clientconfig[u"outbound"][u"settings"][u"vnext"][0][u"users"][0][u"id"]=str(readjson.ConfUUID)
clientconfig[u"outbound"][u"settings"][u"vnext"][0][u"users"][0][u"security"]=str(readjson.ConfSecurity)
clientconfig[u"outbound"][u"streamSettings"]=readjson.ConfStream
if str(readjson.ConfStreamSecurity) == "":
    clientconfig[u"outbound"][u"settings"][u"vnext"][0][u"address"]=str(myip)
else:
    domainfile = file("/usr/local/v2ray.fun/mydomain", "r")
    content = domainfile.read()
    clientconfig[u"outbound"][u"settings"][u"vnext"][0][u"address"] = str(content)
    domainfile.close()
    clientconfig[u"outbound"][u"streamSettings"][u"security"] = "tls"
    clientconfig[u"outbound"][u"streamSettings"][u"tlsSettings"] = {}
#写入客户端配置文件
WriteClientJson()
