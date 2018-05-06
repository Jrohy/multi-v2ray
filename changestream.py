#! /usr/bin/env python
# -*- coding: utf-8 -*-
import readjson
import writejson
import v2rayutil

#读取配置文件信息
mystreamnetwork=str(readjson.ConfStreamNetwork)
if readjson.ConfStreamNetwork=="kcp" :
    if(readjson.ConfStreamHeader=="kcp srtp"):
        mystreamnetwork="mKCP 伪装 FaceTime通话"
    elif(readjson.ConfStreamHeader=="kcp utp"):
        mystreamnetwork="mKCP 伪装 BT下载流量"
    elif(readjson.ConfStreamHeader=="kcp wechat-video"):
        mystreamnetwork="mKCP 伪装 微信视频流量"
    else:
        mystreamnetwork="mKCP"
elif readjson.ConfStreamNetwork=="http":
    mystreamnetwork="HTTP伪装"
elif readjson.ConfStreamNetwork=="ws":
    mystreamnetwork="WebSocket"
elif readjson.ConfStreamNetwork=="h2":
    mystreamnetwork="HTTP/2"

#显示当前配置
print("当前传输方式为：%s") % mystreamnetwork

#选择新的传输方式
print ("请选择新的传输方式：")
print ("1.普通TCP")
print ("2.HTTP伪装")
print ("3.WebSocket流量")
print ("4.普通mKCP")
print ("5.mKCP + srtp")
print ("6.mKCP + utp")
print ("7.mKCP + wechat-video")
print ("8.HTTP/2")

newstreamnetwork=raw_input()

if ( not v2rayutil.is_number(newstreamnetwork)):
    print("请输入数字！")
    exit
else:
    if not (newstreamnetwork > 0 and newstreamnetwork<9):
    	v2rayutil.writeStreamJson(newstreamnetwork)
    else:
        print("请输入有效数字！")
        exit
