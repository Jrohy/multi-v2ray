#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import uuid
import time
import subprocess
import pkg_resources
from functools import wraps
from v2ray_util import run_type
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
        print("{}ing {}...".format(keyword, run_type))
        time.sleep(1)
        if V2ray.docker_status() or keyword == "stop":
            print(ColorStr.green("{} {} success !".format(run_type, keyword)))
        else:
            print(ColorStr.red("{} {} fail !".format(run_type, keyword)))

    @staticmethod
    def run(command, keyword):
        try:
            subprocess.check_output(command, shell=True)
            print("{}ing {}...".format(keyword, run_type))
            time.sleep(2)
            if subprocess.check_output("systemctl is-active {}|grep active".format(run_type), shell=True) or keyword == "stop":
                print(ColorStr.green("{} {} success !".format(run_type, keyword)))
            else:
                raise subprocess.CalledProcessError
        except subprocess.CalledProcessError:
            print(ColorStr.red("{} {} fail !".format(run_type, keyword)))

    @staticmethod
    def docker_status():
        is_running = True
        failed = bytes.decode(subprocess.run('cat /.run.log|grep failed', shell=True, stdout=subprocess.PIPE).stdout)
        running = bytes.decode(subprocess.run('ps aux|grep /etc/{}/config.json'.format(run_type), shell=True, stdout=subprocess.PIPE).stdout)
        if failed or "/usr/bin/{bin}/{bin}".format(bin=run_type) not in running:
            is_running = False
        return is_running

    @staticmethod
    def status():
        if os.path.exists("/.dockerenv"):
            if V2ray.docker_status():
                print(ColorStr.green("{} running..".format(run_type)))
            else:
                print(bytes.decode(subprocess.run('cat /.run.log', shell=True, stdout=subprocess.PIPE).stdout))
                print(ColorStr.yellow("{} stoped..".format(run_type)))
        else:
            subprocess.call("systemctl status {}".format(run_type), shell=True)

    @staticmethod
    def version():
        v2ray_version = bytes.decode(subprocess.check_output("/usr/bin/{bin}/{bin}".format(bin=run_type) + " -version | head -n 1 | awk '{print $2}'", shell=True))
        import v2ray_util
        print("{}: {}".format(run_type, ColorStr.green(v2ray_version)))
        print("v2ray_util: {}".format(ColorStr.green(v2ray_util.__version__)))    

    @staticmethod
    def info():
        from .loader import Loader 
        print(Loader().profile)

    @staticmethod
    def update(version=None):
        if is_ipv6(get_ip()):
            print(ColorStr.yellow(_("ipv6 network not support update {soft} online, please manual donwload {soft} to update!".format(soft=run_type))))
            if run_type == "xray":
                print(ColorStr.fuchsia(_("download Xray-linux-xx.zip and run 'bash <(curl -L -s https://multi.netlify.app/go.sh) -l Xray-linux-xx.zip -x' to update")))
            else:
                print(ColorStr.fuchsia(_("download v2ray-linux-xx.zip and run 'bash <(curl -L -s https://multi.netlify.app/go.sh) -l v2ray-linux-xx.zip' to update")))
            sys.exit(0)
        if os.path.exists("/.dockerenv"):
            V2ray.stop()
        subprocess.Popen("curl -Ls https://multi.netlify.app/go.sh -o temp.sh", shell=True).wait()
        subprocess.Popen("bash temp.sh {} {} && rm -f temp.sh".format("-x" if run_type == "xray" else "", "--version {}".format(version) if version else ""), shell=True).wait()
        if os.path.exists("/.dockerenv"):
            V2ray.start()

    @staticmethod
    def cleanLog():
        subprocess.call("cat /dev/null > /var/log/{}/access.log".format(run_type), shell=True)
        subprocess.call("cat /dev/null > /var/log/{}/error.log".format(run_type), shell=True)
        print(ColorStr.green(_("clean {} log success!".format(run_type))))
        print("")

    @staticmethod
    def log(error_log=False):
        f = subprocess.Popen(['tail','-f', '-n', '100', '/var/log/{}/{}.log'.format(run_type, "error" if error_log else "access")],
                stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        try:
            while True:
                print(bytes.decode(f.stdout.readline().strip()))
        except BaseException:
            print()

    @classmethod
    def restart(cls):
        if os.path.exists("/.dockerenv"):
            V2ray.stop()
            V2ray.start()
        else:
            cls.run("systemctl restart {}".format(run_type), "restart")

    @classmethod
    def start(cls):
        if os.path.exists("/.dockerenv"):
            cls.docker_run("/usr/bin/{bin}/{bin} -config=/etc/{bin}/config.json > /.run.log &".format(bin=run_type), "start")
        else:
            cls.run("systemctl start {}".format(run_type), "start")

    @classmethod
    def stop(cls):
        if os.path.exists("/.dockerenv"):
            cls.docker_run("ps aux|grep /usr/bin/{bin}/{bin}".format(bin=run_type) + "|awk '{print $1}'|xargs  -r kill -9 2>/dev/null", "stop")
        else:
            cls.run("systemctl stop {}".format(run_type), "stop")

    @classmethod
    def check(cls):
        if not os.path.exists("/etc/v2ray_util/util.cfg"):
            subprocess.call("mkdir -p /etc/v2ray_util && cp -f {} /etc/v2ray_util/".format(pkg_resources.resource_filename(__name__, 'util.cfg')), shell=True)
        if not os.path.exists("/usr/bin/{bin}/{bin}".format(bin=run_type)):
            print(ColorStr.yellow(_("check {soft} no install, auto install {soft}..".format(soft=run_type))))
            cls.update()
            cls.new()

    @classmethod
    def remove(cls):
        if os.path.exists("/.dockerenv"):
            print(ColorStr.yellow("docker run don't support remove {}!".format(run_type)))
            return
        cls.stop()
        subprocess.call("systemctl disable {}.service".format(run_type), shell=True)
        subprocess.call("rm -rf /usr/bin/{bin} /etc/systemd/system/{bin}.service".format(bin=run_type), shell=True)
        print(ColorStr.green("Removed {} successfully.".format(run_type)))
        print(ColorStr.blue("If necessary, please remove configuration file and log file manually."))

    @classmethod
    def new(cls):
        subprocess.call("rm -rf /etc/{soft}/config.json && cp {package_path}/server.json /etc/{soft}/config.json".format(soft=run_type, package_path=pkg_resources.resource_filename('v2ray_util', "json_template")), shell=True)
        new_uuid = uuid.uuid1()
        print("new UUID: {}".format(ColorStr.green(str(new_uuid))))
        new_port = random_port(1000, 65535)
        print("new port: {}".format(ColorStr.green(str(new_port))))
        subprocess.call("sed -i \"s/cc4f8d5b-967b-4557-a4b6-bde92965bc27/{uuid}/g\" /etc/{soft}/config.json && sed -i \"s/999999999/{port}/g\" /etc/{soft}/config.json".format(uuid=new_uuid, port=new_port, soft=run_type), shell=True)
        if run_type == "xray":
            subprocess.call("sed -i \"s/v2ray/xray/g\" /etc/xray/config.json", shell=True)
        from ..config_modify import stream
        stream.StreamModifier().random_kcp()
        open_port()
        cls.restart()