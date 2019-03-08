#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import pkg_resources
import random
import shutil
import subprocess
import uuid
from .utils import ColorStr, open_port

service_cmd_fmt = get_service_cmd_fmt()

def get_service_cmd_fmt():
    systemctl = shutil.which('systemctl')
    if systemctl is not None:
        return systemctl + ' {0} v2ray'

    service = shutil.which('service')
    if service is not None:
        return service + ' v2ray {0}'
    else:
        return 'service v2ray {0}'

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
        subprocess.call(service_cmd_fmt.format('status'), shell=True)

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
        print(ColorStr.green("clean v2ray log success!\n"))

    @classmethod
    def restart(cls):
        cls.run(service_cmd_fmt.format('restart'), 'restart')

    @classmethod
    def start(cls):
        cls.run(service_cmd_fmt.format('start'), 'start')

    @classmethod
    def stop(cls):
        cls.run(service_cmd_fmt.format('stop'), 'stop')

    @classmethod
    def check(cls):
        if not os.path.exists("/usr/bin/v2ray/v2ray"):
            print(ColorStr.yellow("check v2ray no install, auto install v2ray.."))
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
