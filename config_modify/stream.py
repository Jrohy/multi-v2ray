#! /usr/bin/env python
# -*- coding: utf-8 -*-
import read_json
import write_json
import v2rayutil

#读取配置文件信息
mystreamnetwork=str(read_json.ConfStreamNetwork)
if read_json.ConfStreamNetwork=="kcp" :
    if(read_json.ConfStreamHeader=="kcp srtp"):
        mystreamnetwork="mKCP + srtp"
    elif(read_json.ConfStreamHeader=="kcp utp"):
        mystreamnetwork="mKCP + utp"
    elif(read_json.ConfStreamHeader=="kcp wechat-video"):
        mystreamnetwork="mKCP + wechat-video"
    elif(read_json.ConfStreamHeader=="kcp dtls"):
        mystreamnetwork="mKCP + dtls"
    else:
        mystreamnetwork="mKCP"
elif read_json.ConfStreamNetwork=="http":
    mystreamnetwork="HTTP伪装"
elif read_json.ConfStreamNetwork=="ws":
    mystreamnetwork="WebSocket"
elif read_json.ConfStreamNetwork=="h2":
    mystreamnetwork="HTTP/2"

#显示当前配置
print ("当前传输方式为：%s") % mystreamnetwork
print ("")
#选择新的传输方式
print ("请选择新的传输方式：")
print ("1.普通TCP")
print ("2.HTTP伪装")
print ("3.WebSocket流量")
print ("4.普通mKCP")
print ("5.mKCP + srtp")
print ("6.mKCP + utp")
print ("7.mKCP + wechat-video")
print ("8.mKCP + dtls")
print ("9.HTTP/2")

newstreamnetwork=raw_input()

if ( not v2rayutil.is_number(newstreamnetwork)):
    print("请输入数字！")
    exit
else:
    if not (newstreamnetwork > 0 and newstreamnetwork < 10):
    	v2rayutil.writeStreamJson(newstreamnetwork)
    else:
        print("请输入有效数字！")
        exit
