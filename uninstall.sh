#!/bin/bash
export PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

#卸载V2ray官方脚本
systemctl stop v2ray  >/dev/null 2>&1
systemctl disable v2ray  >/dev/null 2>&1
service v2ray stop  >/dev/null 2>&1
update-rc.d -f v2ray remove  >/dev/null 2>&1
rm -rf  /etc/v2ray/  >/dev/null 2>&1
rm -rf /usr/bin/v2ray  >/dev/null 2>&1
rm -rf /var/log/v2ray/  >/dev/null 2>&1
rm -rf /lib/systemd/system/v2ray.service  >/dev/null 2>&1
rm -rf /etc/init.d/v2ray  >/dev/null 2>&1

#卸载V2ray.Fun
rm -rf /usr/local/v2ray.fun >/dev/null 2>&1
rm -rf /usr/local/bin/v2ray >/dev/null 2>&1
rm -rf /root/install.sh  >/dev/null 2>&1
echo "卸载完成！"
