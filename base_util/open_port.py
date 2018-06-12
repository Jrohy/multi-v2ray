#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import read_json

multi_user_conf = read_json.multiUserConf
port_set = set([])

for sin_user_conf in multi_user_conf:
    port_set.add(sin_user_conf['port'])

for port in port_set:
    cmd1="iptables -I INPUT -m state --state NEW -m tcp -p tcp --dport " + str(port) +" -j ACCEPT"
    cmd2="iptables -I INPUT -m state --state NEW -m udp -p udp --dport " + str(port) +" -j ACCEPT"
    os.system(cmd1)
    os.system(cmd2)