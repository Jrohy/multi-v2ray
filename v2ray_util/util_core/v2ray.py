#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import subprocess

from .utils import ColorStr

class V2ray:

    @staticmethod
    def run(command, keyword):
        try:
            subprocess.check_output([command])
            ColorStr.green("v2ray {} success !".format(keyword))
        except subprocess.CalledProcessError:
            ColorStr.red("v2ray {} fail !".format(keyword))

    @classmethod
    def restart(cls):
        cls.run("service v2ray restart", "重启")

    @classmethod
    def start(cls):
        cls.run("service v2ray start", "启动")

    @classmethod
    def stop(cls):
        cls.run("service v2ray stop", "停止")

    @staticmethod
    def status():
        os.system("service v2ray status")

    @staticmethod
    def update():
        os.system("bash <(curl -L -s https://install.direct/go.sh)")

    @staticmethod
    def cleanLog():
        os.system("cat /dev/null > /var/log/v2ray/access.log")
        os.system("cat /dev/null > /var/log/v2ray/error.log")
        ColorStr.green("清理v2ray日志成功!\n")