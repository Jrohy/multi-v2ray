#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

start_v2ray_cmd = "service v2ray start >/dev/null 2>&1"
stop_v2ray_cmd = "service v2ray stop >/dev/null 2>&1"

start_nginx_cmd = "service nginx start >/dev/null 2>&1"
stop_nginx_cmd = "service nginx stop >/dev/null 2>&1"

start_httpd_cmd = "service httpd start >/dev/null 2>&1"
stop_httpd_cmd = "service httpd stop >/dev/null 2>&1"

start_apache2_cmd = "service apache2 start >/dev/null 2>&1"
stop_apache2_cmd = "service apache2 stop >/dev/null 2>&1"

def gen_cert(domain):
    if not os.path.exists("/root/.acme.sh/acme.sh"):
        os.system("curl https://get.acme.sh | sh")

    get_ssl_cmd = "bash /root/.acme.sh/acme.sh  --issue -d " +domain +"   --standalone  --keylength ec-256"

    os.system(stop_v2ray_cmd)
    os.system(stop_nginx_cmd)
    os.system(stop_httpd_cmd)
    os.system(stop_apache2_cmd)
    os.system(get_ssl_cmd)
    os.system(start_v2ray_cmd)
    os.system(start_nginx_cmd)
    os.system(start_httpd_cmd)
    os.system(start_apache2_cmd)