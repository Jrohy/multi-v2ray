#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket

from .tls import TLSModifier
from ..util_core.v2ray import restart
from ..util_core.selector import GroupSelector
from ..util_core.writer import StreamWriter, GroupWriter
from ..util_core.utils import StreamType, ColorStr, get_ip, loop_input_choice_number, check_ip, is_ipv4

# https://support.cloudflare.com/hc/en-us/articles/200169156-Identifying-network-ports-compatible-with-Cloudflare-s-proxy
class CDNModifier:
    def __init__(self, group_tag='A', group_index=-1, domain=''):
        self.domain = domain
        self.group_tag = group_tag
        self.group_index = group_index
        if domain:
            StreamWriter(self.group_tag, self.group_index, StreamType.WS).write()

        self.gw = GroupWriter(group_tag, group_index)

    def openHttps(self, port=443):
        '''
        cloudflare cdn proxy https port(443, 2053, 2083, 2087, 2096, 8443)
        '''
        self.gw.write_port(port)
        TLSModifier(self.group_tag, self.group_index, self.domain).turn_on()

def modify():
    port_choice = ""
    gs = GroupSelector(_("modify cdn"))
    group = gs.group

    https_list=(443, 2053, 2083, 2087, 2096, 8443)

    if group == None:
        pass
    else:
        if check_ip(group.ip):
            domain = input(_("please input run cdn mode domain: "))
            if not domain:
                print(ColorStr.yellow(_("domain is empty!")))
                return
        else:
            temp_domain = input(_("this group domain {}, enter to use it or input other domain: ").format(group.ip))
            if temp_domain:
                domain = temp_domain
            else:
                domain = group.ip

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
        print("")
        CDNModifier(group.tag, group.index, domain).openHttps(https_list[port_choice - 1])