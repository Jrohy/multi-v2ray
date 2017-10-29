#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os

start_v2ray_cmd = "service v2ray start >/dev/null 2>&1"
stop_v2ray_cmd = "service v2ray stop >/dev/null 2>&1"

start_nginx_cmd = "service nginx start >/dev/null 2>&1"
stop_nginx_cmd = "service nginx stop >/dev/null 2>&1"

start_httpd_cmd = "service httpd start >/dev/null 2>&1"
stop_httpd_cmd = "service httpd stop >/dev/null 2>&1"



def getssl(domain):
    crt_file = "/root/.acme.sh/"+domain+"_ecc"+"/fullchain.cer"
    key_file = "/root/.acme.sh/"+domain+"_ecc"+"/"+domain+".key"
    get_ssl_cmd = "bash /root/.acme.sh/acme.sh  --issue -d " +domain +"   --standalone  --keylength ec-256"

    #判断是否存在证书
    if os.path.isfile(crt_file) and os.path.isfile(key_file):
        print("证书文件已存在，跳过获取证书阶段。")
    else:
        os.system(stop_v2ray_cmd)
        os.system(stop_nginx_cmd)
        os.system(start_httpd_cmd)
        os.system(get_ssl_cmd)
        os.system(start_v2ray_cmd)
        os.system(start_nginx_cmd)
        os.system(start_httpd_cmd)
        print("证书获取成功！")
