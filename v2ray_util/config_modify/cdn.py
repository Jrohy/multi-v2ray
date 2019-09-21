#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket

from .tls import TLSModifier
from ..util_core.v2ray import restart
from ..util_core.selector import GroupSelector
from ..util_core.writer import StreamWriter, GroupWriter
from ..util_core.utils import StreamType, ColorStr, get_ip

class CDNModifier:
    def __init__(self, group_tag='A', group_index=-1, domain='', fake_domain=''):
        self.domain = domain
        self.group_tag = group_tag
        self.group_index = group_index
        self.__writeWS(fake_domain)

        self.gw = GroupWriter(group_tag, group_index)
    
    def __writeWS(self, fake_domain):
        sw = StreamWriter(self.group_tag, self.group_index, StreamType.WS)
        sw.write(**{'host': fake_domain})

    def openHttp(self):
        '''
        cloudfare cdn proxy 80 port
        '''
        self.gw.write_port("80")
        self.gw.write_domain(self.domain)

    def openHttps(self):
        '''
        cloudfare cdn proxy 443 port
        '''
        self.gw.write_port("443")
        TLSModifier(self.group_tag, self.group_index, self.domain).turn_on()

@restart()
def modify():
    gs = GroupSelector(_("run cdn mode"))
    group = gs.group

    if group == None:
        pass
    else:
        print("")
        print(_("1.80 port + ws"))
        print(_("2.443 port + ws"))
        choice = input(_("please select: "))
        if not choice:
            return
        if not choice in ("1", "2"):
            print(_("input error, please input again"))
            return
            
        fake_domain = input(_("please input ws fake domain(enter to no need): "))
        domain = input(_("please input run cdn mode domain: "))
        if not domain:
            print(ColorStr.yellow(_("domain is empty!")))
            return
        try:
            input_ip = socket.gethostbyname(domain)
        except Exception:
            print(_("domain check error!!!"))
            print("")
            return
        
        if choice == '2':
            local_ip = get_ip()
            print(_("local vps ip address: ") + local_ip + "\n")

            if input_ip != local_ip:
                print(_("domain can't analysis to local ip!!!"))
                print(_("must be close cdn proxy!"))
                print("")
                return

        cm = CDNModifier(group.tag, group.index, domain, fake_domain)

        if choice == '1':
            cm.openHttp()
        elif choice == '2':
            cm.openHttps()

        return True