#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket

from .tls import TLSModifier
from ..util_core.v2ray import restart
from ..util_core.loader import Loader
from ..util_core.writer import StreamWriter, NodeWriter
from ..util_core.utils import StreamType, ColorStr, get_ip, loop_input_choice_number, check_ip, is_ipv4, port_is_use

# https://support.cloudflare.com/hc/en-us/articles/200169156-Identifying-network-ports-compatible-with-Cloudflare-s-proxy
class CDNModifier:
    def __init__(self, domain='', cType=0):
        '''
        cType 0: vmess_ws, 1: vless_ws
        '''
        self.domain = domain
        self.cType = cType          

    @restart(True)
    def open(self, port=443):
        '''
        cloudflare cdn proxy https port(443, 2053, 2083, 2087, 2096, 8443)
        '''
        nw = NodeWriter()
        nw.create_new_port(int(port))
        reload_data = Loader()
        new_group_list = reload_data.profile.group_list
        group = new_group_list[-1]
        TLSModifier(group.tag, group.index, self.domain).turn_on(False)
        if self.cType == 0:
            StreamWriter(group.tag, group.index, StreamType.WS).write()
        elif self.cType == 1:
            StreamWriter(group.tag, group.index, StreamType.VLESS_WS).write()
        return True

def modify():
    port_choice = ""

    https_list=(443, 2053, 2083, 2087, 2096, 8443)

    cdn_protocol_list=('vmess_ws', 'vless_ws')

    domain = input(_("please input run cdn mode domain: "))
    if not domain:
        print(ColorStr.yellow(_("domain is empty!")))
        return

    local_ip = get_ip()
    try:
        if is_ipv4(local_ip):
            input_ip = socket.gethostbyname(domain)
        else:
            input_ip = socket.getaddrinfo(domain, None, socket.AF_INET6)[0][4][0]
    except Exception:
        print(_("domain check error!!!"))
        print("")
        return
    
    print("")
    print(_("local vps ip address: ") + local_ip + "\n")

    if input_ip != local_ip:
        print(_("domain can't analysis to local ip!!!"))
        print(_("must be close cdn proxy!"))
        print("")
        return

    for index, text in enumerate(https_list): 
        print("{}.{}".format(index + 1, text))
    port_choice = loop_input_choice_number(_("please select https port to cdn: "), len(https_list))
    if not port_choice:
        return
    new_port = https_list[port_choice - 1]
    if port_is_use(new_port):
        print("{} port is use!".format(new_port))
        return
    print("")
    for index, text in enumerate(cdn_protocol_list): 
        print("{}.{}".format(index + 1, text))
    cdn_choice = loop_input_choice_number(_("please select protocol to cdn: "), len(cdn_protocol_list))
    if not cdn_choice:
        return
    CDNModifier(domain, cdn_choice - 1).open(new_port)