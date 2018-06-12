#! /usr/bin/env python
# -*- coding: utf-8 -*-
import write_json
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
        write_json.WriteStreamNetwork("tcp","none")
    elif(newstreamnetwork=="2"):
        print("请输入你想要为伪装的域名（不不不需要http）：")
        host=raw_input()
        write_json.WriteStreamNetwork("tcp",str(host))
    elif(newstreamnetwork=="3"):
        print("请输入你的服务器绑定域名（不不不需要http）：")
        host=raw_input()
        write_json.WriteStreamNetwork("ws",str(host))
    elif(newstreamnetwork=="4"):
        write_json.WriteStreamNetwork("mkcp","none")
    elif(newstreamnetwork=="5"):
        write_json.WriteStreamNetwork("mkcp","kcp srtp")
    elif(newstreamnetwork=="6"):
        write_json.WriteStreamNetwork("mkcp","kcp utp")
    elif(newstreamnetwork=="7"):
        write_json.WriteStreamNetwork("mkcp","kcp wechat-video")
    elif(newstreamnetwork=="8"):
        write_json.WriteStreamNetwork("mkcp","kcp dtls")
    elif(newstreamnetwork=="9"):
        write_json.WriteStreamNetwork("h2","none")


def randomStream():
    writeStreamJson(str(random.randint(5,7)))