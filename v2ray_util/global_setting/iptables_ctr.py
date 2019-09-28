#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import subprocess
import pkg_resources

from ..util_core.loader import Loader
from ..util_core.utils import ColorStr, calcul_iptables_traffic

def manage():
    if os.path.exists("/.dockerenv"):
        print(ColorStr.yellow("docker run not support iptables!"))
        return

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

        choice = input(_("please select: "))
        if choice == "1":
            print("")
            for group in group_list:
                print(calcul_iptables_traffic(group.port))
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