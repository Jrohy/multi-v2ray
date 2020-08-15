#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import uuid
import time
import subprocess
import pkg_resources
from functools import wraps
from .utils import ColorStr, open_port, get_ip, is_ipv6, random_port

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
    def docker_run(command, keyword):
        subprocess.run(command, shell=True)
        print("{}ing v2ray...".format(keyword))
        time.sleep(1)
        if V2ray.docker_status() or keyword == "stop":
            print(ColorStr.green("v2ray {} success !".format(keyword)))
        else:
            print(ColorStr.red("v2ray {} fail !".format(keyword)))

    @staticmethod
    def run(command, keyword):
        try:
            subprocess.check_output(command, shell=True)
            print("{}ing v2ray...".format(keyword))
            time.sleep(2)
            if subprocess.check_output("systemctl is-active v2ray|grep active", shell=True) or keyword == "stop":
                print(ColorStr.green("v2ray {} success !".format(keyword)))
            else:
                raise subprocess.CalledProcessError
        except subprocess.CalledProcessError:
            print(ColorStr.red("v2ray {} fail !".format(keyword)))

    @staticmethod
    def docker_status():
        is_running = True
        failed = bytes.decode(subprocess.run('cat /.run.log|grep failed', shell=True, stdout=subprocess.PIPE).stdout)
        running = bytes.decode(subprocess.run('ps aux|grep /etc/v2ray/config.json', shell=True, stdout=subprocess.PIPE).stdout)
        if failed or "/usr/bin/v2ray/v2ray" not in running:
            is_running = False
        return is_running

    @staticmethod
    def status():
        if os.path.exists("/.dockerenv"):
            if V2ray.docker_status():
                print(ColorStr.green("v2ray running.."))
            else:
                print(bytes.decode(subprocess.run('cat /.run.log', shell=True, stdout=subprocess.PIPE).stdout))
                print(ColorStr.yellow("v2ray stoped.."))
        else:
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
        if is_ipv6(get_ip()):
            print(ColorStr.yellow(_("ipv6 network not support update v2ray online, please manual donwload v2ray to update!")))
            print(ColorStr.fuchsia(_("download v2ray-linux-xx.zip and run 'bash <(curl -L -s https://multi.netlify.app/go.sh) -l v2ray-linux-xx.zip' to update")))
            return
        if os.path.exists("/.dockerenv"):
            V2ray.stop()
        subprocess.Popen("curl -L -s https://multi.netlify.app/go.sh|bash", shell=True).wait()
        if os.path.exists("/.dockerenv"):
            V2ray.start()

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
        if os.path.exists("/.dockerenv"):
            V2ray.stop()
            V2ray.start()
        else:
            cls.run("systemctl restart v2ray", "restart")

    @classmethod
    def start(cls):
        if os.path.exists("/.dockerenv"):
            cls.docker_run("/usr/bin/v2ray/v2ray -config=/etc/v2ray/config.json > /.run.log &", "start")
        else:
            cls.run("systemctl start v2ray", "start")

    @classmethod
    def stop(cls):
        if os.path.exists("/.dockerenv"):
            cls.docker_run('''ps aux|grep "/usr/bin/v2ray/v2ray"|awk '{print $1}'|xargs  -r kill -9 2>/dev/null''', "stop")
        else:
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
            if is_ipv6(get_ip()):
                subprocess.Popen("curl -Ls https://multi.netlify.app/go.sh -o temp.sh", shell=True).wait()
                subprocess.Popen("bash temp.sh --source jsdelivr && rm -f temp.sh", shell=True).wait()
            else:
                cls.update()
            cls.new()

    @classmethod
    def new(cls):
        subprocess.call("rm -rf /etc/v2ray/config.json && cp {}/server.json /etc/v2ray/config.json".format(pkg_resources.resource_filename('v2ray_util', "json_template")), shell=True)
        new_uuid = uuid.uuid1()
        print("new UUID: {}".format(ColorStr.green(str(new_uuid))))
        new_port = random_port(1000, 65535)
        print("new port: {}".format(ColorStr.green(str(new_port))))
        subprocess.call("sed -i \"s/cc4f8d5b-967b-4557-a4b6-bde92965bc27/{0}/g\" /etc/v2ray/config.json && sed -i \"s/999999999/{1}/g\" /etc/v2ray/config.json".format(new_uuid, new_port), shell=True)
        from ..config_modify import stream
        stream.StreamModifier().random_kcp()
        open_port()
        cls.restart()