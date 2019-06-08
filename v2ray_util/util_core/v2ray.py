#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import uuid
import random
import subprocess
import pkg_resources
from .utils import ColorStr, open_port

class V2ray:

    @staticmethod
    def run(command, keyword):
        try:
            subprocess.check_output(command, shell=True)
            open_port()
            print(ColorStr.green("v2ray {} success !".format(keyword)))
        except subprocess.CalledProcessError:
            print(ColorStr.red("v2ray {} fail !".format(keyword)))

    @staticmethod
    def status():
        subprocess.call("service v2ray status", shell=True)

    @staticmethod
    def version():
        v2ray_version = bytes.decode(subprocess.check_output("/usr/bin/v2ray/v2ray -version | head -n 1 | awk '{print $2}'", shell=True))
        import v2ray_util
        print("v2ray: {}".format(ColorStr.green(v2ray_version)))
        print("v2ray_util: {}".format(ColorStr.green(v2ray_util.__version__)))   

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
        print(ColorStr.green(_("clean v2ray log success!")))
        print("")

    @staticmethod
    def log():
        import subprocess
        f = subprocess.Popen(['tail','-f', '/var/log/v2ray/access.log'],
                stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        while True:
            print(bytes.decode(f.stdout.readline().strip()))

    @classmethod
    def restart(cls):
        cls.run("service v2ray restart", "restart")

    @classmethod
    def start(cls):
        cls.run("service v2ray start", "start")

    @classmethod
    def stop(cls):
        cls.run("service v2ray stop", "stop")

    @classmethod
    def convert(cls):
        from .converter import ConfigConverter

    @classmethod
    def check(cls):
        if not os.path.exists("/etc/v2ray_util/util.cfg"):
            subprocess.call("mkdir -p /etc/v2ray_util && cp -f {} /etc/v2ray_util/".format(pkg_resources.resource_filename(__name__, 'util.cfg')), shell=True)
        if not os.path.exists("/usr/bin/v2ray/v2ray"):
            print(ColorStr.yellow(_("check v2ray no install, auto install v2ray..")))
            cls.update()
            cls.new()

    @classmethod
    def new(cls):
        subprocess.call("rm -rf /etc/v2ray/config.json && cp {}/server.json /etc/v2ray/config.json".format(pkg_resources.resource_filename('v2ray_util', "json_template")), shell=True)
        new_uuid = uuid.uuid1()
        print("new UUID: {}".format(ColorStr.green(str(new_uuid))))
        random_port = random.randint(1000, 65535)
        print("new port: {}".format(ColorStr.green(str(random_port))))
        subprocess.call("sed -i \"s/cc4f8d5b-967b-4557-a4b6-bde92965bc27/{0}/g\" /etc/v2ray/config.json && sed -i \"s/999999999/{1}/g\" /etc/v2ray/config.json".format(new_uuid, random_port), shell=True)
        from ..config_modify import stream
        stream.StreamModifier().random_kcp()
        cls.restart()