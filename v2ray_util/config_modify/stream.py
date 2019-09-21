#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import string

from ..util_core.v2ray import restart
from ..util_core.writer import StreamWriter
from ..util_core.selector import GroupSelector, CommonSelector
from ..util_core.group import Mtproto, SS
from ..util_core.utils import StreamType, header_type_list, ColorStr

from .ss import SSFactory

class StreamModifier:
    def __init__(self, group_tag='A', group_index=-1):
        self.stream_type = [
            (StreamType.TCP, "TCP"), 
            (StreamType.TCP_HOST, "Fake HTTP"), 
            (StreamType.WS, "WebSocket"), 
            (StreamType.KCP, "mKCP"), 
            (StreamType.KCP_SRTP, "mKCP + srtp"), 
            (StreamType.KCP_UTP, "mKCP + utp"), 
            (StreamType.KCP_WECHAT, "mKCP + wechat-video"),
            (StreamType.KCP_DTLS, "mKCP + dtls"), 
            (StreamType.KCP_WG, "mKCP + wireguard"), 
            (StreamType.H2, "HTTP/2"), 
            (StreamType.SOCKS, "Socks5"), 
            (StreamType.MTPROTO, "MTProto"), 
            (StreamType.SS, "Shadowsocks"),
            (StreamType.QUIC, "Quic")
        ]
        self.group_tag = group_tag
        self.group_index = group_index

    def select(self, index):
        sw = StreamWriter(self.group_tag, self.group_index, self.stream_type[index][0])
        kw = {}
        if index == 0 or (index >= 3 and index <= 9) or index == 11:
            pass
        elif index == 1 or index == 2:
            host = input(_("please input fake domain: "))
            kw['host'] = host
        elif index == 10:
            user = input(_("please input socks user: "))
            password = input(_("please input socks password: "))
            if user == "" or password == "":
                print(_("socks user or password is null!!"))
                exit(-1)
            kw = {'user': user, 'pass': password}
        elif index == 12:
            sf = SSFactory()
            kw = {"method": sf.get_method(), "password": sf.get_password()}
        elif index == 13:
            key = ""
            security_list = ('none', "aes-128-gcm", "chacha20-poly1305")
            print("")
            security = CommonSelector(security_list, _("please select ss method: ")).select()
            if security != "none":
                key = ''.join(random.sample(string.ascii_letters + string.digits, 8))
                new_pass = input('{} {}, {}'.format(_("random generate password"), key, _("enter to use, or input customize password: ")))
                if new_pass:
                    key = new_pass
                    
            print("")
            header = CommonSelector(header_type_list(), _("please select fake header: ")).select()
            kw = {'security': security, 'key': key, 'header': header}
        sw.write(**kw)

    def random_kcp(self):
        kcp_list = ('mKCP + srtp', 'mKCP + utp', 'mKCP + wechat-video', 'mKCP + dtls')
        choice = random.randint(4, 7)
        print("{}: {} \n".format(_("random generate (srtp | wechat-video | utp | dtls) fake header, new protocol"), ColorStr.green(kcp_list[choice - 4])))
        self.select(choice)

@restart()
def modify():
    gs = GroupSelector(_('modify protocol'))
    group = gs.group

    if group == None:
        pass
    else:
        sm = StreamModifier(group.tag, group.index)

        print("{}: {}".format(_("group protocol"), group.node_list[0].stream()))
        print ("")
        for index, stream_type in enumerate(sm.stream_type):
            print("{0}.{1}".format(index + 1, stream_type[1]))

        choice = input()

        if not choice.isdecimal():
            print(_("please input number!"))
        else:
            choice = int(choice)
            if choice > 0 and choice <= len(sm.stream_type):
                if (sm.stream_type[choice - 1][1] == "MTProto" or sm.stream_type[choice - 1][1] == "Shadowsocks") and group.tls == 'tls':
                    print(_("V2ray MTProto/Shadowsocks not support https, close tls success!"))
                sm.select(choice - 1)
                print(_("modify protocol success"))
                return True
            else:
                print(_("input out of range!!"))