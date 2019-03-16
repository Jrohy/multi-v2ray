#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import os

from ..util_core.writer import GroupWriter
from ..util_core.group import Mtproto, SS
from ..util_core.selector import GroupSelector
from ..util_core.utils import get_ip, get_domain_by_crt_file, gen_cert

class TLSModifier:
    def __init__(self, group_tag, group_index):
        self.writer = GroupWriter(group_tag, group_index)
    
    def turn_on(self):
        print("1. Let’s Encrypt certificate(auto create, please prepare domain)")
        print("2. Customize certificate(prepare certificate file paths)\n")
        choice=input("please select: ")
        if choice == "1":
            local_ip = get_ip()
            print("local vps ip address: " + local_ip + "\n")
            input_domain=input("please input your vps domain: ")
            try:
                input_ip = socket.gethostbyname(input_domain)
            except Exception:
                print("\ndomain check error!!!\n")
                return
            if input_ip != local_ip:
                print("\ndomain can't analysis to local ip!!!\n")
                return

            print("")
            print("auto generate SSL certificate, please wait..")
            gen_cert(input_domain)
            crt_file = "/root/.acme.sh/" + input_domain +"_ecc"+ "/fullchain.cer"
            key_file = "/root/.acme.sh/" + input_domain +"_ecc"+ "/"+ input_domain +".key"

            self.writer.write_tls(True, crt_file=crt_file, key_file=key_file, domain=input_domain)

        elif choice == "2":
            crt_file = input("please input certificate cert file path: ")
            key_file = input("please input certificate key file path: ")
            if not os.path.exists(crt_file) or not os.path.exists(key_file):
                print("certificate cert or key not exist!\n")
                return
            domain = input("please input the certificate cert file domain: ")
            if not domain:
                print("domain is null!\n")
                return
            self.writer.write_tls(True, crt_file=crt_file, key_file=key_file, domain=domain)
        else:
            print("input error!\n")
    
    def turn_off(self):
        self.writer.write_tls(False)

def modify():
    gs = GroupSelector('modify TLS')
    group = gs.group

    if group == None:
        exit(-1)
    else:
        if type(group.node_list[0]) == Mtproto or type(group.node_list[0]) == SS:
            print("\nv2ray MTProto/Shadowsocks protocol not support https!!!\n")
            exit(-1)
        tm = TLSModifier(group.tag, group.index)
        tls_status = 'open' if group.tls == 'tls' else 'close'
        print("group tls status: {}\n".format(tls_status))
        print("")
        print("1.open TLS")
        print("2.close TLS")
        choice = input("please select: ")
        if choice == '1':
            tm.turn_on()
        elif choice == '2':
            tm.turn_off()
        else:
            print("input error, please try again!")