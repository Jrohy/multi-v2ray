#! /usr/bin/env python
# -*- coding: utf-8 -*-
import readjson
import writejson

#判断是否为数字的函数
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

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

#显示当前配置
print("当前传输方式为：%s") % mystreamnetwork

#选择新的传输方式
print ("请选择新的传输方式：")
print ("1.普通TCP")
print ("2.HTTP伪装")
print ("3.WebSocket流量")
print ("4.普通mKCP")
print ("5.mKCP 伪装 FaceTime通话")
print ("6.mKCP 伪装 BT下载流量")
print ("7.mKCP 伪装 微信视频流量")

newstreamnetwork=raw_input()

if ( not is_number(newstreamnetwork)):
    print("请输入数字！")
    exit
else:
    if not (newstreamnetwork > 0 and newstreamnetwork<8):
        
        if(newstreamnetwork=="1"):
            writejson.WriteStreamNetwork("tcp","none")
        elif(newstreamnetwork=="2"):
            print("请输入你想要为伪装的域名（不不不需要http）：")
            host=raw_input()
            writejson.WriteStreamNetwork("tcp",str(host))
        elif(newstreamnetwork=="3"):
            print("请输入你的服务器绑定域名（不不不需要http）：")
            host=raw_input()
            writejson.WriteStreamNetwork("ws",str(host))
        elif(newstreamnetwork=="4"):
            writejson.WriteStreamNetwork("mkcp","none")
        elif(newstreamnetwork=="5"):
            writejson.WriteStreamNetwork("mkcp","kcp srtp")
        elif(newstreamnetwork=="6"):
            writejson.WriteStreamNetwork("mkcp","kcp utp")
        elif(newstreamnetwork=="7"):
            writejson.WriteStreamNetwork("mkcp","kcp wechat-video")
    else:
        print("请输入有效数字！")
        exit
