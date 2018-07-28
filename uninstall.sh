#!/bin/bash
export PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

#检查系统信息
if [ -f /etc/redhat-release ];then
        OS='CentOS'
    elif [ ! -z "`cat /etc/issue | grep bian`" ];then
        OS='Debian'
    elif [ ! -z "`cat /etc/issue | grep Ubuntu`" ];then
        OS='Ubuntu'
    else
        echo "Not support OS, Please reinstall OS and retry!"
        exit 1
fi

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

#卸载multi-v2ray
rm -rf /usr/local/multi-v2ray >/dev/null 2>&1
rm -rf /usr/local/bin/v2ray >/dev/null 2>&1
rm -rf /root/install.sh  >/dev/null 2>&1

#删除v2ray定时更新任务
crontab -l|sed '/SHELL=/d;/v2ray/d' > crontab.txt
crontab crontab.txt >/dev/null 2>&1
rm -f crontab.txt >/dev/null 2>&1

if [[ "${OS}" == "CentOS" ]];then
    service crond restart >/dev/null 2>&1
else
    service cron restart >/dev/null 2>&1
fi

#删除multi-v2ray模块搜索路径
sed -i '/multi-v2ray/d' ~/.bashrc
source ~/.bashrc

echo "卸载完成！"
