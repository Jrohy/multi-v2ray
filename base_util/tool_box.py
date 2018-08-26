#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import os
import re
from OpenSSL import crypto

def is_number(s):
    """
    判断是否为数字的函数
    """
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

def get_ip():
    """
    获取本地ip
    """
    my_ip = urllib.request.urlopen('http://api.ipify.org').read()
    return bytes.decode(my_ip)

def port_is_use(port):
    """
    判断端口是否占用
    """
    cmd = "lsof -i:" + str(port)
    result = os.popen(cmd).readlines()
    return result != []

def is_email(email):
    """
    判断是否是邮箱格式
    """
    str=r'^[\w\.]+@[\w]+\.[\w]+$'
    return re.match(str, email)

def get_domain_by_crt_file(crt_path):
    """
    通过证书文件获取域名, 证书文件有误或不存在则返回空
    """
    try:
        cert = crypto.load_certificate(crypto.FILETYPE_PEM, open(crt_path).read())
    except:
        return
    return cert.get_subject().CN

def bytes_2_human_readable(number_of_bytes, precision=1):
    """
    流量bytes转换为kb, mb, gb等单位
    """
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