#! /usr/bin/env python
# -*- coding: utf-8 -*-
import readjson
import getssl
import writejson
import urllib2
import socket

def get_ip():
    myip = urllib2.urlopen('http://members.3322.org/dyndns/getip').read()
    myip = myip.strip()
    return str(myip)

def open_tls():
    print("请将您的域名解析到本VPS的IP地址，否则程序会出错！！")
    local_ip = get_ip()
    print("本机器IP地址为：" + local_ip)
    inputdomain=str(raw_input("请输入您绑定的域名："))
    try:
        input_ip = socket.gethostbyname(inputdomain)
    except Exception:
        print("域名检测错误!!!")
        return
    if input_ip != local_ip:
        print("输入的域名与本机ip不符!!!")
        return

    print("")
    print("正在获取SSL证书，请稍等。")
    getssl.getssl(inputdomain)
    writejson.WriteTLS("on",inputdomain)
    print("操作完成！")

def close_tls():
    writejson.WriteTLS("off","")
    print("操作完成！\n")
    print("已重置为 mKCP 伪装 FaceTime通话(srtp)的传输模式")

if (readjson.ConfStreamSecurity=="tls"):
    mystreamsecurity="TLS：开启"
else:
    mystreamsecurity="TLS：关闭"

print("当前状态：\n" + mystreamsecurity)
print("")
print("1.开启TLS")
print("2.关闭TLS")

choice = int(input("请输入数字选择功能："))

if choice == 1:
    open_tls()
elif choice == 2:
    close_tls()
else:
    print("输入错误，请重试！")
