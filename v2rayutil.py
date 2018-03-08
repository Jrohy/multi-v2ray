#! /usr/bin/env python
# -*- coding: utf-8 -*-
import writejson
import random

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

def writeStreamJson(newstreamnetwork):
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


def randomStream():
    writeStreamJson(str(random.randint(5,7)))