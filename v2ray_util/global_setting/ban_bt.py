#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ..util_core.loader import Loader
from ..util_core.v2ray import restart
from ..util_core.writer import GlobalWriter

@restart()
def manage():
    loader = Loader()

    profile = loader.profile

    print("{}: {}".format(_("Ban BT status"), profile.ban_bt))

    choice = input(_("Ban BT?(y/n): ")).lower()

    if not choice:
        return

    ban_bt = True if choice == 'y' else False

    gw = GlobalWriter(profile.group_list)

    gw.write_ban_bittorrent(ban_bt)

    print(_("modify success!"))
    
    return True