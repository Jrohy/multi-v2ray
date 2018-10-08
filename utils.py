#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import os
import re
from enum import Enum, unique
from OpenSSL import crypto

@unique
class Color(Enum):
    """
    终端显示颜色 枚举类
    """
   # 显示格式: \033[显示方式;前景色;背景色m
    # 只写一个字段表示前景色,背景色默认
    RED = '\033[31m'       # 红色
    GREEN = '\033[32m'     # 绿色
    YELLOW = '\033[33m'    # 黄色
    BLUE = '\033[34m'      # 蓝色
    FUCHSIA = '\033[35m'   # 紫红色
    CYAN = '\033[36m'      # 青蓝色
    WHITE = '\033[37m'     # 白色
    #: no color
    RESET = '\033[0m'      # 终端默认颜色

def color_str(color: Color, str: str) -> str:
    """
    返回有色字符串
    """
    return '{}{}{}'.format(
        color.value,
        str,
        Color.RESET.value
    )

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

def gen_cert(domain):
    service_name = ["v2ray", "nginx", "httpd", "apache2"]
    start_cmd = "service {} start >/dev/null 2>&1"
    stop_cmd = "service {} stop >/dev/null 2>&1"

    if not os.path.exists("/root/.acme.sh/acme.sh"):
        os.system("curl https://get.acme.sh | sh")

    get_ssl_cmd = "bash /root/.acme.sh/acme.sh  --issue -d " + domain + "   --standalone  --keylength ec-256"

    for name in service_name:
        os.system(stop_cmd.format(name))
    os.system(get_ssl_cmd)
    for name in service_name:
        os.system(start_cmd.format(name))

def open_port():

    from loader import Loader

    group_list = Loader().profile.group_list

    port_set = set([group.port for group in group_list])

    for port in port_set:
        cmd1="iptables -I INPUT -m state --state NEW -m tcp -p tcp --dport " + str(port) +" -j ACCEPT"
        cmd2="iptables -I INPUT -m state --state NEW -m udp -p udp --dport " + str(port) +" -j ACCEPT"
        os.system(cmd1)
        os.system(cmd2)