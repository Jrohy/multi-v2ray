#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import os

from ..util_core.v2ray import restart
from ..util_core.writer import GroupWriter
from ..util_core.group import Mtproto, SS
from ..util_core.selector import GroupSelector
from ..util_core.utils import get_ip, gen_cert

class TLSModifier:
    def __init__(self, group_tag, group_index, domain=''):
        self.domain = domain
        self.writer = GroupWriter(group_tag, group_index)
    
    def turn_on(self):
        print(_("1. Let's Encrypt certificate(auto create, please prepare domain)"))
        print(_("2. Customize certificate(prepare certificate file paths)"))
        print("")
        choice=input(_("please select: "))
        input_domain = self.domain
        if choice == "1":
            if not input_domain:
                local_ip = get_ip()
                print(_("local vps ip address: ") + local_ip + "\n")
                input_domain = input(_("please input your vps domain: "))
                try:
                    input_ip = socket.gethostbyname(input_domain)
                except Exception:
                    print(_("domain check error!!!"))
                    print("")
                    return
                if input_ip != local_ip:
                    print(_("domain can't analysis to local ip!!!"))
                    print("")
                    return

            print("")
            print(_("auto generate SSL certificate, please wait.."))
            gen_cert(input_domain)
            crt_file = "/root/.acme.sh/" + input_domain +"_ecc"+ "/fullchain.cer"
            key_file = "/root/.acme.sh/" + input_domain +"_ecc"+ "/"+ input_domain +".key"

            self.writer.write_tls(True, crt_file=crt_file, key_file=key_file, domain=input_domain)

        elif choice == "2":
            crt_file = input(_("please input certificate cert file path: "))
            key_file = input(_("please input certificate key file path: "))
            if not os.path.exists(crt_file) or not os.path.exists(key_file):
                print(_("certificate cert or key not exist!"))
                return
            if not input_domain:
                input_domain = input(_("please input the certificate cert file domain: "))
                if not input_domain:
                    print(_("domain is null!"))
                    return
            self.writer.write_tls(True, crt_file=crt_file, key_file=key_file, domain=input_domain)
        else:
            print(_("input error!"))
    
    def turn_off(self):
        self.writer.write_tls(False)

@restart()
def modify():
    gs = GroupSelector(_('modify tls'))
    group = gs.group

    if group == None:
        pass
    else:
        if type(group.node_list[0]) == Mtproto or type(group.node_list[0]) == SS:
            print(_("V2ray MTProto/Shadowsocks protocol not support https!!!"))
            print("")
            return
        tm = TLSModifier(group.tag, group.index)
        tls_status = 'open' if group.tls == 'tls' else 'close'
        print("{}: {}\n".format(_("group tls status"), tls_status))
        print("")
        print(_("1.open TLS"))
        print(_("2.close TLS"))
        choice = input(_("please select: "))
        if not choice:
            return
        if not choice in ("1", "2"):
            print(_("input error, please input again"))
            return

        if choice == '1':
            tm.turn_on()
        elif choice == '2':
            tm.turn_off()
            
        return True