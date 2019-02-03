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
        print("1. Let’s Encrypt 生成证书(准备域名)")
        print("2. 自定义已存在的其他路径的证书(准备证书文件路径)\n")
        choice=input("请选择使用证书方式: ")
        if choice == "1":
            print("\n请将您的域名解析到本VPS的IP地址，否则程序会出错！！\n")
            local_ip = get_ip()
            print("本机器IP地址为：" + local_ip + "\n")
            input_domain=input("请输入您绑定的域名：")
            try:
                input_ip = socket.gethostbyname(input_domain)
            except Exception:
                print("\n域名检测错误!!!\n")
                return
            if input_ip != local_ip:
                print("\n输入的域名与本机ip不符!!!\n")
                return

            print("")
            print("正在获取SSL证书，请稍等。。。")
            gen_cert(input_domain)
            crt_file = "/root/.acme.sh/" + input_domain +"_ecc"+ "/fullchain.cer"
            key_file = "/root/.acme.sh/" + input_domain +"_ecc"+ "/"+ input_domain +".key"

            self.writer.write_tls(True, crt_file=crt_file, key_file=key_file, domain=input_domain)

        elif choice == "2":
            crt_file = input("请输入证书cert文件路径: ")
            key_file = input("请输入证书key文件路径: ")
            if not os.path.exists(crt_file) or not os.path.exists(key_file):
                print("证书crt文件或者key文件指定路径不存在!\n")
                return
            domain = get_domain_by_crt_file(crt_file)
            if not domain:
                print("证书文件有误!\n")
                return
            self.writer.write_tls(True, crt_file=crt_file, key_file=key_file, domain=domain)
        else:
            print("输入有误!\n")
    
    def turn_off(self):
        self.writer.write_tls(False)

def modify():
    gs = GroupSelector('修改TLS')
    group = gs.group

    if group == None:
        exit(-1)
    else:
        if type(group.node_list[0]) == Mtproto or type(group.node_list[0]) == SS:
            print("\nv2ray MTProto/Shadowsocks协议不支持配置https!!!\n")
            exit(-1)
        tm = TLSModifier(group.tag, group.index)
        tls_status = '开启' if group.tls == 'tls' else '关闭'
        print("当前选择组节点状态：{}\n".format(tls_status))
        print("")
        print("1.开启TLS")
        print("2.关闭TLS")
        choice = input("请输入数字选择功能：")
        if choice == '1':
            tm.turn_on()
        elif choice == '2':
            tm.turn_off()
        else:
            print("输入错误，请重试！")