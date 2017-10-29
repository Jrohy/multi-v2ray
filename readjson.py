#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json

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
ConfStreamKcpSettings=ConfStream[u'kcpSettings']
ConfStreamNetwork=ConfStream[u"network"]
ConfStreamSecurity=ConfStream[u"security"]

if ConfStreamNetwork=="kcp" :
    if ConfStreamKcpSettings.has_key('header'):
        ConfStreamHeader=ConfStreamKcpSettings[u"header"][u'type']
    else:
        ConfStreamHeader="none"