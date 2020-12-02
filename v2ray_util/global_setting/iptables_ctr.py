#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import pkg_resources

from ..util_core.loader import Loader
from ..util_core.utils import ColorStr, calcul_iptables_traffic, readchar

def manage():
    
    loader = Loader()

    profile = loader.profile

    group_list = profile.group_list

    while True:
        print("")
        print(_("Iptables Traffic Statistics"))
        print("")
        print(_("1.check statistics result"))
        print("")
        print(_("2.reset special port statistics"))
        print("")

        choice = readchar(_("please select: "))
        if choice == "1":
            print("")
            ipv6 = True if profile.network == "ipv6" else False
            for group in group_list:
                print(calcul_iptables_traffic(group.port, ipv6))
            print("")

        elif choice == "2":
            port = input(_("please input reset port:"))
            if port and port.isnumeric():
                subprocess.call("bash {0} {1}".format(pkg_resources.resource_filename(__name__, "clean_traffic.sh"), str(port)), shell=True)
                print(ColorStr.green(_("reset success!")))
            else:
                print(ColorStr.red(_("input error!")))
        else:
            break