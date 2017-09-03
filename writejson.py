#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json


#打开配置文件
jsonfile = file("/etc/v2ray/config.json")
config = json.load(jsonfile)

#写入配置文件
def Write():
    myjsondump=json.dumps(config,indent=1)
    openjsonfile=file("/etc/v2ray/config.json","w+")
    openjsonfile.writelines(myjsondump)
    openjsonfile.close()
    
#更改UUID
def WriteUUID(myuuid):
    config[u"inbound"][u"settings"][u"clients"][0][u"id"]=str(myuuid)
    Write()
    
#更改端口
def WritePort(myport):
    config[u"inbound"][u"port"]=int(myport)
    Write()

#更改加密方式
def WriteSecurity(mysecurity):
    config[u"inbound"][u"settings"][u"clients"][0][u"security"]=str(mysecurity)
    Write()
    
#更改底层传输设置
def WriteStreamNetwork(network,para):
    
    if (network == "tcp" and para=="none"):
        streamfile=file("/usr/local/v2ray.fun/json_template/tcp.json")
        tcp=json.load(streamfile)
        config[u"inbound"][u"streamSettings"]=tcp
        Write()
    if (network == "tcp" and para != "none"):
        streamfile=file("/usr/local/v2ray.fun/json_template/http.json")
        http=json.load(streamfile)
        http[u"tcpSettings"][u"header"][u"request"][u"headers"][u"Host"]=para
        config[u"inbound"][u"streamSettings"]=http
        Write()
    if (network == "ws"):
        streamfile=file("/usr/local/v2ray.fun/json_template/ws.json")
        ws=json.load(streamfile)
        config[u"inbound"][u"streamSettings"]=ws
        Write()
    if (network == "mkcp" and para=="none"):
        streamfile=file("/usr/local/v2ray.fun/json_template/kcp.json")
        kcp=json.load(streamfile)
        config[u"inbound"][u"streamSettings"]=kcp
        Write()
    if (network == "mkcp" and para=="kcp utp"):
        streamfile=file("/usr/local/v2ray.fun/json_template/kcp_utp.json")
        utp=json.load(streamfile)
        config[u"inbound"][u"streamSettings"]=utp
        Write()
    if (network == "mkcp" and para=="kcp srtp"):
        streamfile=file("/usr/local/v2ray.fun/json_template/kcp_srtp.json")
        srtp=json.load(streamfile)
        config[u"inbound"][u"streamSettings"]=srtp
        Write()    
        
    if (network == "mkcp" and para=="kcp wechat-video"):
        streamfile=file("/usr/local/v2ray.fun/json_template/kcp_wechat.json")
        wechat=json.load(streamfile)
        config[u"inbound"][u"streamSettings"]=wechat
        Write()  