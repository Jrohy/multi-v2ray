#! /usr/bin/env python
# -*- coding: utf-8 -*-
import readjson
import getssl
import writejson
import urllib2
import socket

def get_ip():
    myip = urllib2.urlopen('http://api.ipify.org').read()
    myip = myip.strip()
    return str(myip)

def open_tls():
    print("\n请将您的域名解析到本VPS的IP地址，否则程序会出错！！\n")
    local_ip = get_ip()
    print("本机器IP地址为：" + local_ip + "\n")
    inputdomain=str(raw_input("请输入您绑定的域名："))
    try:
        input_ip = socket.gethostbyname(inputdomain)
    except Exception:
        print("\n域名检测错误!!!\n")
        return
    if input_ip != local_ip:
        print("\n输入的域名与本机ip不符!!!\n")
        return

    print("")
    print("正在获取SSL证书，请稍等。")
    getssl.getssl(inputdomain)
    writejson.WriteTLS("on",inputdomain)
    print("\n操作完成！\n")

def close_tls():
    writejson.WriteTLS("off","")
    print("操作完成！\n")

def show_tip():
    if (readjson.ConfStreamSecurity=="tls"):
        mystreamsecurity="TLS：开启"
    else:
        mystreamsecurity="TLS：关闭"

    print("当前状态：\n" + mystreamsecurity)
    print("")
    print("1.开启TLS")
    print("2.关闭TLS")

    choice = raw_input("请输入数字选择功能：")

    if choice == "1":
        open_tls()
    elif choice == "2":
        close_tls()
    else:
        print("输入错误，请重试！")
