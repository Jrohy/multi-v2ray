#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random

from writer import StreamWriter, StreamType
from selector import GroupSelector
from group import Mtproto, SS

from config_modify.ss import SSFactory

class StreamModifier:
    def __init__(self, group_tag='A', group_index=-1):
        self.stream_type = [
            (StreamType.TCP, "普通TCP"), 
            (StreamType.TCP_HOST, "HTTP伪装"), 
            (StreamType.WS, "WebSocket流量"), 
            (StreamType.KCP, "普通mKCP"), 
            (StreamType.KCP_SRTP, "mKCP + srtp"), 
            (StreamType.KCP_UTP, "mKCP + utp"), 
            (StreamType.KCP_WECHAT, "mKCP + wechat-video"),
            (StreamType.KCP_DTLS, "mKCP + dtls"), 
            (StreamType.KCP_WG, "mKCP + wireguard"), 
            (StreamType.H2, "HTTP/2"), 
            (StreamType.SOCKS, "Socks5"), 
            (StreamType.MTPROTO, "MTProto"), 
            (StreamType.SS, "Shadowsocks")
        ]
        self.group_tag = group_tag
        self.group_index = group_index

    def select(self, index):
        sw = StreamWriter(self.group_tag, self.group_index, self.stream_type[index][0])
        kw = {}
        if index == 0 or (index >= 3 and index < 9) or index == 11:
            pass
        elif index == 1 or index == 2:
            host = input("请输入你想要为伪装的域名（不不不需要http）：")
            kw['host'] = host
        elif index == 9:
            pass
        elif index == 10:
            user = input("请输入socks的用户名: ")
            password = input("请输入socks的密码: ")
            if user == "" or password == "":
                print("socks的用户名或者密码不能为空")
                exit(-1)
            kw = {'user': user, 'pass': password}
        elif index == 12:
            sf = SSFactory()
            kw = {"method": sf.get_method(), "password": sf.get_password()}
        sw.write(**kw)

    def random_kcp(self):
        kcp_list = ('mKCP + srtp', 'mKCP + utp', 'mKCP + wechat-video', 'mKCP + dtls')
        choice = random.randint(4, 7)
        print("随机一种 (srtp | wechat-video | utp | dtls) header伪装, 当前生成 {} \n".format(kcp_list[choice - 4]))
        self.select(choice)

if __name__ == '__main__':

    gs = GroupSelector('修改传输方式')
    group = gs.group

    if group == None:
        exit(-1)
    else:
        sm = StreamModifier(group.tag, group.index)

        print("当前组的传输方式为：{}".format(group.node_list[0].stream()))
        print ("")
        for index, stream_type in enumerate(sm.stream_type):
            print("{0}.{1}".format(index + 1, stream_type[1]))

        choice = input()

        if not choice.isdecimal():
            print("请输入数字！")
        else:
            choice = int(choice)
            if choice > 0 and choice <= len(sm.stream_type):
                if (sm.stream_type[choice - 1][1] == "MTProto" or sm.stream_type[choice - 1][1] == "Shadowsocks") and group.tls == 'tls':
                    print("v2ray MTProto/Shadowsocks不支持https, 关闭tls成功!")
                sm.select(choice - 1)
                print("传输模式修改成功！")
            else:
                print("请输入符合范围的数字！")