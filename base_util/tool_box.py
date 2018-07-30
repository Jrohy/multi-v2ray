#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import os
import re

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

#获取本地ip
def get_ip():
    my_ip = urllib.request.urlopen('http://api.ipify.org').read()
    return bytes.decode(my_ip)

#判断端口是否占用
def port_is_use(port):
    cmd = "lsof -i:" + str(port)
    result = os.popen(cmd).readlines()
    return result != []

#判断是否是邮箱格式
def is_email(email):
    str=r'^[\w\.]+@[\w]+\.[\w]+$'
    return re.match(str, email)

#流量bytes转换为kb, mb, gb等单位
def bytes_2_human_readable(number_of_bytes, precision=1):
    if number_of_bytes < 0:
        raise ValueError("!!! number_of_bytes can't be smaller than 0 !!!")
 
    step_to_greater_unit = 1024.
 
    number_of_bytes = float(number_of_bytes)
    unit = 'bytes'
 
    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'KB'
 
    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'MB'
 
    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'GB'
 
    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'TB'
 
    number_of_bytes = round(number_of_bytes, precision)
 
    return str(number_of_bytes) + ' ' + unit