#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .tls import TLSModifier
from ..util_core.selector import GroupSelector
from ..util_core.writer import StreamWriter, GroupWriter
from ..util_core.utils import StreamType, ColorStr

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

def modify():
    gs = GroupSelector("修改为cdn模式")
    group = gs.group

    if group == None:
        exit(-1)
    else:
        print("")
        print("1.修改为cdn模式 80端口 + ws")
        print("2.修改为cdn模式 443端口 + ws")
        choice = input(_("please select: "))
        domain = input("请输入走cdn的域名: ")
        fake_domain = input("请输入ws要伪装的域名(不伪装直接回车): ")
        cm = CDNModifier(group.tag, group.index, domain, fake_domain)

        if choice == '1':
            cm.openHttp()
        elif choice == '2':
            cm.openHttps()
        else:
            print(_("input error, please input again"))