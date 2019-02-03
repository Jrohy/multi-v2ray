#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess

from .utils import ColorStr

class V2ray:

    @staticmethod
    def run(command, keyword):
        try:
            subprocess.check_output(command, shell=True)
            print(ColorStr.green("v2ray {} success !".format(keyword)))
        except subprocess.CalledProcessError:
            print(ColorStr.red("v2ray {} fail !".format(keyword)))

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
        subprocess.call("service v2ray status", shell=True)

    @classmethod
    def update(cls):
        subprocess.Popen("curl -L -s https://install.direct/go.sh|bash", shell=True).wait()

    @staticmethod
    def cleanLog():
        subprocess.call("cat /dev/null > /var/log/v2ray/access.log", shell=True)
        subprocess.call("cat /dev/null > /var/log/v2ray/error.log", shell=True)
        print(ColorStr.green("清理v2ray日志成功!\n"))