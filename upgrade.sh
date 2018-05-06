#!/bin/bash
export PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

#fonts color
Green="\033[32m" 
Red="\033[31m" 
Yellow="\033[33m"
GreenBG="\033[42;37m"
RedBG="\033[41;37m"
Font="\033[0m"

#notification information
Info="${Green}[信息]${Font}"
OK="${Green}[OK]${Font}"
Error="${Red}[错误]${Font}"

#重装V2ray.fun
mv /usr/local/v2ray.fun/mydomain ~
rm -rf /usr/local/v2ray.fun
cd /usr/local/
git clone https://github.com/Jrohy/v2ray.fun
cd /usr/local/v2ray.fun/
chmod +x *.py
mv -f ~/mydomain .

#重装操作菜单
rm -rf /usr/local/bin/v2ray
cp /usr/local/v2ray.fun/v2ray /usr/local/bin/
chmod +x /usr/local/bin/v2ray

#时间同步
systemctl stop ntp &>/dev/null
echo -e "${Info} 正在进行时间同步 ${Font}"
ntpdate time.nist.gov
if [[ $? -eq 0 ]];then 
    echo -e "${OK} 时间同步成功 ${Font}"
    echo -e "${OK} 当前系统时间 `date -R`${Font}"
    sleep 1
else
    echo -e "${Error} ${RedBG} 时间同步失败，可以手动执行命令同步:\n${Font}"
    echo - "${Yellow}ntpdate time.nist.gov${Font}"
fi 

#更新Vray主程序
bash <(curl -L -s https://install.direct/go.sh)

clear

echo -e "${OK}脚本已更新！${Font}\n"

echo "V2ray配置信息:"
#安装完后显示v2ray的配置信息，用于快速部署
python /usr/local/v2ray.fun/serverinfo.py
