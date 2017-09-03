#!/bin/bash
export PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

#检查是否为Root
[ $(id -u) != "0" ] && { echo "Error: You must be root to run this script"; exit 1; }

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

#禁用SELinux
if [ -s /etc/selinux/config ] && grep 'SELINUX=enforcing' /etc/selinux/config; then
    sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config
    setenforce 0
fi

#安装依赖
if [[ ${OS} == 'CentOS' ]];then
	yum install curl wget unzip git ntp ntpdate lrzsz python -y
else
	apt-get update
	apt-get install curl unzip git ntp wget ntpdate python lrzsz -y
fi

#克隆V2ray.fun项目
cd /usr/local/
git clone https://github.com/FunctionClub/v2ray.fun

#安装V2ray主程序
bash <(curl -L -s https://install.direct/go.sh)

#配置V2ray初始环境
mv /usr/local/v2ray.fun/v2ray /usr/local/bin
mv /usr/local/v2ray.fun/v2ray /usr/bin
chmod +x /usr/bin/v2ray
chmod +x /usr/local/bin/v2ray
rm -rf /etc/v2ray/config.json
mv /usr/local/v2ray.fun/json_template/server.json /etc/v2ray/config.json
python /usr/local/v2ray.fun/genclient.py
python /usr/local/v2ray.fun/openport.py
service v2ray restart

echo "V2ray.fun 安装成功！By: 雨落无声"
echo "输入 v2ray 回车即可使用"