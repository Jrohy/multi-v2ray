#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import uuid
import random
import subprocess
import pkg_resources
from .utils import ColorStr

class V2ray:

    @staticmethod
    def run(command, keyword):
        try:
            subprocess.check_output(command, shell=True)
            print(ColorStr.green("v2ray {} success !".format(keyword)))
        except subprocess.CalledProcessError:
            print(ColorStr.red("v2ray {} fail !".format(keyword)))

    @staticmethod
    def status():
        subprocess.call("service v2ray status", shell=True)

    @staticmethod
    def info():
        from .loader import Loader 
        print(Loader().profile)

    @staticmethod
    def update():
        subprocess.Popen("curl -L -s https://install.direct/go.sh|bash", shell=True).wait()

    @staticmethod
    def cleanLog():
        subprocess.call("cat /dev/null > /var/log/v2ray/access.log", shell=True)
        subprocess.call("cat /dev/null > /var/log/v2ray/error.log", shell=True)
        print(ColorStr.green("清理v2ray日志成功!\n"))

    @classmethod
    def restart(cls):
        cls.run("service v2ray restart", "重启")

    @classmethod
    def start(cls):
        cls.run("service v2ray start", "启动")

    @classmethod
    def stop(cls):
        cls.run("service v2ray stop", "停止")

    @classmethod
    def check(cls):
        if not os.path.exists("/usr/bin/v2ray/v2ray"):
            print(ColorStr.yellow("检测到v2ray未安装, 正在自动安装.."))
            cls.update()
            cls.new()

    @classmethod
    def new(cls):
        subprocess.call("rm -rf /etc/v2ray/config.json && cp {}/server.json /etc/v2ray/config.json".format(pkg_resources.resource_filename('v2ray_util', "json_template")), shell=True)
        new_uuid = uuid.uuid1()
        print("新的UUID为：{}".format(ColorStr.green(str(new_uuid))))
        random_port = random.randint(1000, 65535)
        print("产生随机端口: {}".format(ColorStr.green(str(random_port))))
        subprocess.call("sed -i \"s/cc4f8d5b-967b-4557-a4b6-bde92965bc27/{0}/g\" /etc/v2ray/config.json && sed -i \"s/999999999/{1}/g\" /etc/v2ray/config.json".format(new_uuid, random_port), shell=True)
        from ..config_modify import stream
        stream.StreamModifier().random_kcp()
        cls.restart()