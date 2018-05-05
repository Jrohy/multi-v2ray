#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import urllib2

#打开配置文件
jsonfile = file("/etc/v2ray/config.json")
config = json.load(jsonfile)

#读取配置文件大框架
ConfInbound=config[u"inbound"]
ConfOutbound=config[u"outbound"]
ConfInboundDetour=config[u"inboundDetour"]
ConfOutboundDetour=config[u"outboundDetour"]
ConfDns=config[u"dns"]
ConfRouting=config[u"routing"]

#读取传入配置细节部分
ConfPort=ConfInbound[u"port"]
ConfUUID=ConfInbound[u"settings"][u"clients"][0][u"id"]
ConfSecurity=ConfInbound[u"settings"][u"clients"][0][u"security"]
ConfAlterId=ConfInbound[u"settings"][u"clients"][0][u"alterId"]
ConfStream=ConfInbound[u"streamSettings"]
ConfStreamKcpSettings=ConfStream[u"kcpSettings"]
ConfStreamHttp2Settings=ConfStream[u"httpSettings"]
ConfStreamNetwork=ConfStream[u"network"]
ConfStreamSecurity=ConfStream[u"security"]

if ConfStreamNetwork=="kcp" :
    if ConfStreamKcpSettings.has_key('header'):
        ConfStreamHeader=ConfStreamKcpSettings[u"header"][u'type']
    else:
        ConfStreamHeader="none"

if ConfInbound[u"settings"][u"ip"]==None:
	#获取本机IP地址
	myip = urllib2.urlopen('http://api.ipify.org').read()
	ConfIP = myip.strip()
else:
	ConfIP=ConfInbound[u"settings"][u"ip"]


if "detour" in ConfInbound[u"settings"]:
    ConfDyp="开启,alterId为 %s" % ConfInboundDetour[0][u"settings"][u"default"][u"alterId"]
else:
    ConfDyp="关闭"
 
if ConfStreamHttp2Settings != None:
    ConfPath=ConfStreamHttp2Settings[u"path"]
else:
    ConfPath="none"