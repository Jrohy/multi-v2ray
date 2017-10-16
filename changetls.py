#! /usr/bin/env python
# -*- coding: utf-8 -*-
import readjson
import getssl
import writejson
import urllib2

def get_ip():
    myip = urllib2.urlopen('http://members.3322.org/dyndns/getip').read()
    myip = myip.strip()
    return str(myip)

def open_tls():
    print("请将您的域名解析到本VPS的IP地址，否则程序会出错！！")
    print("本机器IP地址为：" + get_ip())
    inputdomain=str(raw_input("请输入您绑定的域名："))
    print("")
    print("正在获取SSL证书，请稍等。")
    getssl.getssl(inputdomain)
    writejson.WriteTLS("on",inputdomain)
    print("操作完成！")

def close_tls():
    writejson.WriteTLS("off","")
    print("操作完成！")

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
