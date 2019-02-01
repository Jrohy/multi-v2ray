#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ..util_core.loader import Loader
from ..util_core.writer import GlobalWriter

if __name__ == '__main__':
    loader = Loader()

    profile = loader.profile

    print("当前禁止BT状态: {}".format(profile.ban_bt))

    choice = input("是否禁止BT(y/n)：").lower()

    ban_bt = True if choice == 'y' else False

    gw = GlobalWriter(profile.group_list)

    gw.write_ban_bittorrent(ban_bt)

    print("修改成功!")