#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ..util_core.loader import Loader
from ..util_core.writer import GlobalWriter

def manage():
    loader = Loader()

    profile = loader.profile

    print("Ban BT status: {}".format(profile.ban_bt))

    choice = input("Ban BT?(y/n)").lower()

    ban_bt = True if choice == 'y' else False

    gw = GlobalWriter(profile.group_list)

    gw.write_ban_bittorrent(ban_bt)

    print("modify success!")