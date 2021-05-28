#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import string

from v2ray_util import run_type
from ..util_core.v2ray import restart
from ..util_core.writer import StreamWriter, GroupWriter
from ..util_core.selector import GroupSelector, CommonSelector
from ..util_core.utils import StreamType, header_type_list, ColorStr, all_port, xtls_flow, readchar

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
            (StreamType.QUIC, "Quic"),
            (StreamType.VLESS_KCP, "VLESS + mkcp"),
            (StreamType.VLESS_UTP, "VLESS + mKCP + utp"),
            (StreamType.VLESS_SRTP, "VLESS + mKCP + srtp"),
            (StreamType.VLESS_WECHAT, "VLESS + mKCP + wechat-video"),
            (StreamType.VLESS_DTLS, "VLESS + mKCP + dtls"),
            (StreamType.VLESS_WG, "VLESS + mKCP + wireguard"),
            (StreamType.VLESS_TCP, "VLESS_TCP"),
            (StreamType.VLESS_TLS, "VLESS_TLS"),
            (StreamType.VLESS_WS, "VLESS_WS"),
            (StreamType.VLESS_XTLS, "VLESS_XTLS"),
            (StreamType.VLESS_GRPC, "VLESS_GRPC"),
            (StreamType.TROJAN, "Trojan"),
        ]
        self.group_tag = group_tag
        self.group_index = group_index

    def select(self, sType):
        sw = StreamWriter(self.group_tag, self.group_index, sType)
        kw = {}
        if sType in (StreamType.TCP_HOST, StreamType.WS):
            host = input(_("please input fake domain: "))
            kw['host'] = host
        elif sType == StreamType.SOCKS:
            user = input(_("please input socks user: "))
            password = input(_("please input socks password: "))
            if user == "" or password == "":
                print(_("socks user or password is null!!"))
                exit(-1)
            kw = {'user': user, 'pass': password}
        elif sType == StreamType.SS:
            sf = SSFactory()
            kw = {"method": sf.get_method(), "password": sf.get_password()}
        elif sType == StreamType.QUIC:
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
        elif sType in (StreamType.VLESS_TLS, StreamType.VLESS_WS, StreamType.VLESS_XTLS, StreamType.VLESS_GRPC):
            port_set = all_port()
            if not "443" in port_set:
                print()
                print(ColorStr.yellow(_("auto switch 443 port..")))
                gw = GroupWriter(self.group_tag, self.group_index)
                gw.write_port(443)
                sw = StreamWriter(self.group_tag, self.group_index, sType)
            if sType == StreamType.VLESS_WS:
                host = input(_("please input fake domain: "))
                kw['host'] = host
            elif sType == StreamType.VLESS_XTLS:
                flow_list = xtls_flow()
                print("")
                flow = CommonSelector(flow_list, _("please select xtls flow type: ")).select()
                kw = {'flow': flow}
            elif sType == StreamType.VLESS_GRPC and run_type == "xray":
                choice = readchar(_("open xray grpc multiMode?(y/n): ")).lower()
                if choice == 'y':
                    kw = {'mode': 'multi'}
                
        elif sType == StreamType.TROJAN:
            port_set = all_port()
            if not "443" in port_set:
                print()
                print(ColorStr.yellow(_("auto switch 443 port..")))
                gw = GroupWriter(self.group_tag, self.group_index)
                gw.write_port(443)
                sw = StreamWriter(self.group_tag, self.group_index, sType)
            random_pass = ''.join(random.sample(string.digits + string.ascii_letters, 8))
            tip = _("create random trojan user password:") + ColorStr.cyan(random_pass) + _(", enter to use or input new password: ")
            password = input(tip)
            if password == "":
                password = random_pass
            kw['password'] = password
        sw.write(**kw)

    def random_kcp(self):
        kcp_list = (StreamType.KCP_SRTP, StreamType.KCP_UTP, StreamType.KCP_WECHAT, StreamType.KCP_DTLS, StreamType.KCP_WG)
        choice = random.randint(0, 4)
        print("{}: {} \n".format(_("random generate (srtp | wechat-video | utp | dtls | wireguard) fake header, new protocol"), ColorStr.green(kcp_list[choice].value)))
        self.select(kcp_list[choice])

@restart()
def modify(group=None, sType=None):
    need_restart = False
    if group == None:
        need_restart = True
        gs = GroupSelector(_('modify protocol'))
        group = gs.group

    if group == None:
        pass
    else:
        sm = StreamModifier(group.tag, group.index)

        if sType != None:
            sm.select([v for v in StreamType if v.value == sType][0])
            print(_("modify protocol success"))
            return

        if need_restart:
            print("")
            print("{}: {}".format(_("group protocol"), group.node_list[0].stream()))

        print("")
        for index, stream_type in enumerate(sm.stream_type):
            print("{0}.{1}".format(index + 1, stream_type[1]))

        print("")
        choice = input(_("please select new protocol: "))

        if not choice.isdecimal():
            print(_("please input number!"))
        else:
            choice = int(choice)
            if choice > 0 and choice <= len(sm.stream_type):
                if sm.stream_type[choice - 1][1] in ("MTProto", "Shadowsocks") and group.tls in ('tls', 'xtls'):
                    print(_("{} MTProto/Shadowsocks not support https, close tls success!".format(run_type.capitalize())))
                sm.select(sm.stream_type[choice - 1][0])
                print(_("modify protocol success"))
                if need_restart:
                    return True