#! /usr/bin/env python
# -*- coding: utf-8 -*-

import readjson
import urllib2
import base64
import json
#获取本机IP地址
myip = urllib2.urlopen('http://api.ipify.org').read()
myip = myip.strip()

#判断传输配置
mystreamnetwork=str(readjson.ConfStreamNetwork)

if readjson.ConfStreamNetwork=="kcp" :
    if(readjson.ConfStreamHeader=="utp"):
        mystreamnetwork="mKCP 伪装 BT下载流量"
    elif(readjson.ConfStreamHeader=="srtp"):
        mystreamnetwork="mKCP 伪装 FaceTime通话"
    elif(readjson.ConfStreamHeader=="wechat-video"):
        mystreamnetwork="mKCP 伪装 微信视频流量"
    else:
        mystreamnetwork="mKCP"
elif readjson.ConfStreamNetwork=="http":
    mystreamnetwork="HTTP伪装"
elif readjson.ConfStreamNetwork=="ws":
    mystreamnetwork="WebSocket"

if (readjson.ConfStreamSecurity=="tls"):
    mystreamsecurity="TLS：开启"
else:
    mystreamsecurity="TLS：关闭"

#输出信息
print("服务器IP：%s") % str(myip)
print("主端口：%s") % str(readjson.ConfPort)
print("UUID：%s") % str(readjson.ConfUUID)
print("alter ID: %s") % str(readjson.ConfAlterId)
print("加密方式：%s") % str(readjson.ConfSecurity)
print("传输方式：%s") % str(mystreamnetwork)
print("%s") % str(mystreamsecurity)

#生成vmess字符串
jsonfile = file("/usr/local/v2ray.fun/json_template/vmess.json")
config = json.load(jsonfile)
config["add"]=str(myip)
config["port"]=str(readjson.ConfPort)
config["id"]=str(readjson.ConfUUID)
config["aid"]=str(readjson.ConfAlterId)
config["net"]=str(readjson.ConfStreamNetwork)
if readjson.ConfStreamNetwork=="kcp":
    config["type"]=str(readjson.ConfStreamHeader)
print(config)
base64Str = base64.encodestring(str(config))
base64Str = ''.join(base64Str.split())
print("vmess://%s") % base64Str