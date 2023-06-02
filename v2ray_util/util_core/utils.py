#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import sys
import tty
import socket
import string
import random
import termios
import pkg_resources
import urllib.request
from enum import Enum, unique

class ColorStr:
    RED = '\033[31m'       # 红色
    GREEN = '\033[32m'     # 绿色
    YELLOW = '\033[33m'    # 黄色
    BLUE = '\033[34m'      # 蓝色
    FUCHSIA = '\033[35m'   # 紫红色
    CYAN = '\033[36m'      # 青蓝色
    WHITE = '\033[37m'     # 白色
    #: no color
    RESET = '\033[0m'      # 终端默认颜色

    @classmethod
    def red(cls, s):
        return cls.RED + s + cls.RESET

    @classmethod
    def green(cls, s):
        return cls.GREEN + s + cls.RESET

    @classmethod
    def yellow(cls, s):
        return cls.YELLOW + s + cls.RESET

    @classmethod
    def blue(cls, s):
        return cls.BLUE + s + cls.RESET

    @classmethod
    def cyan(cls, s):
        return cls.CYAN + s + cls.RESET

    @classmethod
    def fuchsia(cls, s):
        return cls.FUCHSIA + s + cls.RESET

    @classmethod
    def white(cls, s):
        return cls.WHITE + s + cls.RESET

@unique
class StreamType(Enum):
    TCP = 'tcp'
    TCP_HOST = 'tcp_host'
    SOCKS = 'socks'
    SS = 'ss'
    MTPROTO = 'mtproto'
    H2 = 'h2'
    WS = 'ws'
    GRPC = 'grpc'
    QUIC = 'quic'
    KCP = 'kcp'
    KCP_UTP = 'utp'
    KCP_SRTP = 'srtp'
    KCP_DTLS = 'dtls'
    KCP_WECHAT = 'wechat'
    KCP_WG = 'wireguard'
    VLESS_KCP = 'vless_kcp'
    VLESS_UTP = 'vless_utp'
    VLESS_SRTP = 'vless_srtp'
    VLESS_DTLS = 'vless_dtls'
    VLESS_WECHAT = 'vless_wechat'
    VLESS_WG = 'vless_wireguard'
    VLESS_TCP = 'vless_tcp'
    VLESS_TLS = 'vless_tls'
    VLESS_WS = 'vless_ws'
    VLESS_GRPC = 'vless_grpc'
    VLESS_REALITY = 'vless_reality'
    TROJAN = 'trojan'

def header_type_list():
    return ("none", "srtp", "utp", "wechat-video", "dtls", "wireguard")

def ss_method():
    return ("aes-256-gcm", "aes-128-gcm", "chacha20-poly1305")

def xtls_flow():
    return ("xtls-rprx-vision", "none")

def get_ip():
    """
    获取本地ip
    """
    my_ip = ""
    try:
        my_ip = urllib.request.urlopen('http://api.ipify.org').read()
    except Exception:
        my_ip = urllib.request.urlopen('http://icanhazip.com').read()
    return bytes.decode(my_ip).strip()

def port_is_use(port):
    """
    判断端口是否占用
    """
    tcp_use, udp_use = False, False
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    u = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.settimeout(3)
    tcp_use = s.connect_ex(('127.0.0.1', int(port))) == 0
    try:
        u.bind(('127.0.0.1', int(port)))
    except:
        udp_use = True
    finally:
        u.close()
    return tcp_use or udp_use

def random_port(start_port, end_port):
    while True:
        random_port = random.randint(start_port, end_port)
        if not port_is_use(random_port):
            return random_port

def is_email(email):
    """
    判断是否是邮箱格式
    """
    str = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
    return re.match(str, email)

def is_ipv4(ip):
    try:
        socket.inet_pton(socket.AF_INET, ip)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(ip)
        except socket.error:
            return False
        return ip.count('.') == 3
    except socket.error:  # not a valid ip
        return False
    return True
 
def is_ipv6(ip):
    try:
        socket.inet_pton(socket.AF_INET6, ip)
    except socket.error:  # not a valid ip
        return False
    return True
 
def check_ip(ip):
    return is_ipv4(ip) or is_ipv6(ip)

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

def gen_cert(domain, cert_type, email=""):
    local_ip = get_ip()
    service_name = ["nginx", "httpd", "apache2"]
    start_cmd = "systemctl start {}  >/dev/null 2>&1"
    stop_cmd = "systemctl stop {} >/dev/null 2>&1"

    if not os.path.exists("/root/.acme.sh/acme.sh"):
        if ":" in local_ip:
            if not os.path.exists("/root/.acme.sh/"):
                os.makedirs("/root/.acme.sh")
            os.system("curl https://acme-install.netlify.app/acme.sh -o /root/.acme.sh/acme.sh")
        else:
            os.system("curl https://get.acme.sh | sh")

    open_port(80)
    if int(os.popen("/root/.acme.sh/acme.sh -v|tr -cd '[0-9]'").read()) < 300:
        os.system("/root/.acme.sh/acme.sh --upgrade")
    if cert_type in ("buypass", "zerossl"):
        os.system("bash /root/.acme.sh/acme.sh --server {} --register-account -m {}".format(cert_type, email))
    get_ssl_cmd = "bash /root/.acme.sh/acme.sh --issue -d " + domain + " --debug --standalone --keylength ec-256 --server " + cert_type
    if len(os.popen("/root/.acme.sh/acme.sh --list|grep {}|grep -i {}".format(domain, cert_type)).readlines()) == 0:
        get_ssl_cmd += " --force"
    if ":" in local_ip:
        get_ssl_cmd += " --listen-v6"
    if cert_type == "buypass":
        get_ssl_cmd += " --days 170"

    if not os.path.exists("/.dockerenv"):
        for name in service_name:
            os.system(stop_cmd.format(name))
    os.system(get_ssl_cmd)
    if not os.path.exists("/.dockerenv"):
        for name in service_name:
            os.system(start_cmd.format(name))

def calcul_iptables_traffic(port, ipv6=False):
    network = "1" if ipv6 else ""
    traffic_result = os.popen("bash {0} {1} {2}".format(pkg_resources.resource_filename("v2ray_util", "global_setting/calcul_traffic.sh"), str(port), network)).readlines()
    if traffic_result:
        traffic_list = traffic_result[0].split()
        upload_traffic = bytes_2_human_readable(int(traffic_list[0]), 2)
        download_traffic = bytes_2_human_readable(int(traffic_list[1]), 2)
        total_traffic = bytes_2_human_readable(int(traffic_list[2]), 2)
        return "{0}:  upload:{1} download:{2} total:{3}".format(ColorStr.green(str(port)), 
                ColorStr.cyan(upload_traffic), ColorStr.cyan(download_traffic), ColorStr.cyan(total_traffic))

def clean_iptables(port):
    import platform
    from .loader import Loader

    iptable_way = "iptables" if Loader().profile.network == "ipv4" else "ip6tables" 

    clean_cmd = "{} -D {} {}"
    check_cmd = "%s -nvL %s --line-number 2>/dev/null|grep -w \"%s\"|awk '{print $1}'|sort -r"
    firewall_clean_cmd = "firewall-cmd --zone=public --remove-port={}/tcp --remove-port={}/udp --permanent >/dev/null 2>&1"

    if "centos-8" in platform.platform():
        os.system("{}-save -c > /etc/sysconfig/iptables 2>/dev/null".format(iptable_way))
        os.system(firewall_clean_cmd.format(str(port), str(port)))
        os.system("firewall-cmd --reload >/dev/null 2>&1")
        os.system("{}-restore -c < /etc/sysconfig/iptables".format(iptable_way))
    input_result = os.popen(check_cmd % (iptable_way, "INPUT", str(port))).readlines()
    for line in input_result:
        os.system(clean_cmd.format(iptable_way, "INPUT", str(line)))

    output_result = os.popen(check_cmd % (iptable_way, "OUTPUT", str(port))).readlines()
    for line in output_result:
        os.system(clean_cmd.format(iptable_way, "OUTPUT", str(line)))

def x25519_key(private_key=None):
    gen_cmd="/usr/bin/xray/xray x25519"
    if private_key:
        gen_cmd = "{} -i '{}'".format(gen_cmd, private_key)
    gen_result = os.popen(gen_cmd + "|awk -F ':' '{print $2}'|sed 's/ //g'").readlines()
    return list(map(lambda x: x.strip(), gen_result))

def all_port():
    from .loader import Loader
    profile = Loader().profile
    group_list = profile.group_list
    return set([group.port for group in group_list])

def iptables_open(iptable_way, port):
    check_cmd = "{} -nvL --line-number 2>/dev/null|grep -w \"{}\""
    input_cmd = "{} -I INPUT -p {} --dport {} -j ACCEPT"
    output_cmd = "{} -I OUTPUT -p {} --sport {}"
    if len(os.popen(check_cmd.format(iptable_way, port)).readlines()) > 0:
        return
    os.system(input_cmd.format(iptable_way, "tcp", port))
    os.system(input_cmd.format(iptable_way, "udp", port))
    os.system(output_cmd.format(iptable_way, "tcp", port))
    os.system(output_cmd.format(iptable_way, "udp", port))

def open_port(openport=-1):
    import platform
    from .loader import Loader

    iptable_way = "iptables" if Loader().profile.network == "ipv4" else "ip6tables"

    is_centos8 = True if "centos-8" in platform.platform() else False
    firewall_open_cmd = "firewall-cmd --zone=public --add-port={}/tcp --add-port={}/udp --permanent >/dev/null 2>&1"

    port_set = all_port()

    if openport != -1:
        port_str = str(openport)
        if is_centos8:
            os.system("{}-save -c > /etc/sysconfig/iptables 2>/dev/null".format(iptable_way))
            os.system(firewall_open_cmd.format(port_str, port_str))
            os.system("firewall-cmd --reload >/dev/null 2>&1")
            os.system("{}-restore -c < /etc/sysconfig/iptables".format(iptable_way))
        else:
            iptables_open(iptable_way, port_str)
    else:
        if is_centos8:
            os.system("{}-save -c > /etc/sysconfig/iptables 2>/dev/null".format(iptable_way))
            for port in port_set:
                os.system(firewall_open_cmd.format(str(port), str(port)))
            os.system("firewall-cmd --reload >/dev/null 2>&1") 
            os.system("{}-restore -c < /etc/sysconfig/iptables".format(iptable_way)) 
        for port in port_set:
            iptables_open(iptable_way, str(port))
    os.system("{}-save -c > /root/.iptables 2>/dev/null".format(iptable_way))

def random_email():
    domain = ['163', 'qq', 'sina', '126', 'gmail', 'outlook', 'icloud']
    core_email = "@{}.com".format(random.choice(domain))
    return ''.join(random.sample(string.ascii_letters + string.digits, 8)) + core_email

def loop_input_choice_number(input_tip, length):
    """
    循环输入选择的序号,直到符合规定为止
    """
    while True:
        print("")
        if length >= 10:
            choice = input(input_tip)
        else:
            choice = readchar(input_tip)
        if not choice:
            return
        if choice.isnumeric():
            choice = int(choice)
        else:
            print(ColorStr.red(_("input error, please input again")))
            continue
        if (choice <= length and choice > 0):
            return choice
        else:
            print(ColorStr.red(_("input error, please input again")))

def readchar(prompt=""):
    if prompt:
        sys.stdout.write(prompt)
        sys.stdout.flush()
        
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    print(ch)
    return ch.strip()