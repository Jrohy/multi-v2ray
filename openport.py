#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import readjson


cmd1="iptables -I INPUT -m state --state NEW -m tcp -p tcp --dport " + str(readjson.ConfPort) +" -j ACCEPT"
cmd2="iptables -I INPUT -m state --state NEW -m udp -p udp --dport " + str(readjson.ConfPort) +" -j ACCEPT"
os.system(cmd1)
os.system(cmd2)