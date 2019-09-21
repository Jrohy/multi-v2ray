#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import uuid
import time
import random
import subprocess
import pkg_resources
from functools import wraps
from .utils import ColorStr, open_port

def restart(port_open=False):
    """
    运行函数/方法后重启v2ray的装饰器
    """  
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kw):
            result = func(*args, **kw)
            if port_open:
                open_port()
            if result:
                V2ray.restart()
        return wrapper
    return decorate

class V2ray:

    @staticmethod
    def run(command, keyword):
        try:
            subprocess.check_output(command, shell=True)
            open_port()
            print("{}ing v2ray...".format(keyword))
            time.sleep(2)
            if subprocess.check_output("systemctl is-active v2ray|grep active", shell=True) or keyword == "stop":
                print(ColorStr.green("v2ray {} success !".format(keyword)))
            else:
                raise subprocess.CalledProcessError
        except subprocess.CalledProcessError:
            print(ColorStr.red("v2ray {} fail !".format(keyword)))

    @staticmethod
    def status():
        subprocess.call("systemctl status v2ray", shell=True)

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
        f = subprocess.Popen(['tail','-f', '-n', '100', '/var/log/v2ray/access.log'],
                stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        while True:
            print(bytes.decode(f.stdout.readline().strip()))

    @classmethod
    def restart(cls):
        cls.run("systemctl restart v2ray", "restart")

    @classmethod
    def start(cls):
        cls.run("systemctl start v2ray", "start")

    @classmethod
    def stop(cls):
        cls.run("systemctl stop v2ray", "stop")

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