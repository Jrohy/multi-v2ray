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

#定时任务北京执行时间(0~23)
BeijingUpdateTime=3

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

#设置定时升级任务
plan_update(){
    #计算北京时间早上3点时VPS的实际时间
    originTimeZone=$(date -R|awk '{printf"%d",$6}')
    localTimeZone=${originTimeZone%00}
    beijingZone=8
    diffZone=$[$beijingZone-$localTimeZone]
    localTime=$[$BeijingUpdateTime-$diffZone]
    if [ $localTime -lt 0 ];then
        localTime=$[24+$localTime]
    elif [ $localTime -ge 24 ];then
        localTime=$[$localTime-24]
    fi
	echo -e "${Info} 北京时间${BeijingUpdateTime}点，VPS时间为${localTime}点 ${Font}\n"

    oldCrontab=$(crontab -l)
    echo "SHELL=/bin/bash" >> crontab.txt
    echo "${oldCrontab}" >> crontab.txt
	echo "0 ${localTime} * * * bash <(curl -L -s https://install.direct/go.sh) | tee -a /root/v2rayUpdate.log && service v2ray restart" >> crontab.txt
	crontab crontab.txt
	sleep 1
	if [[ "${OS}" == "CentOS" ]];then
        service crond restart
	else
		service cron restart
	fi
	rm -f crontab.txt
	echo -e "${OK} 成功配置每天北京时间${BeijingUpdateTime}点自动升级V2ray内核任务 ${Font}\n"
}

[[ -z $(crontab -l|grep v2ray) ]] && isOpen="关闭" || isOpen="开启"

echo -e "当前定时更新任务状态: ${isOpen}\n" 

echo -e ""
echo -e "1.开启定时更新任务\n"
echo -e "2.关闭定时更新任务\n"
echo -e "Tip: 开启定时更新v2ray的更新时间为每天北京时间3:00更新"

while :; do echo
    read -n1 -p "请选择： " choice
    if [[ ! $choice =~ ^[1-2]$ ]]; then
        if [[ -z ${choice} ]];then
            bash /usr/local/bin/v2ray
            exit 0
        fi
        echo "输入错误! 请输入正确的数字!"
    else
        echo -e "\n"
        break
    fi
done

if [[ ${choice} == 1 ]]; then
    if [[ ${isOpen} == "开启" ]]; then
        echo -e "${Info}当前定时更新已开启,无需重复操作!\n"
        bash /usr/local/bin/v2ray
        exit 0
    fi
    #设置定时任务
    plan_update
else 
    #删除v2ray定时更新任务
    crontab -l|sed '/SHELL=/d;/v2ray/d' > crontab.txt
    crontab crontab.txt >/dev/null 2>&1
    rm -f crontab.txt >/dev/null 2>&1
    if [[ "${OS}" == "CentOS" ]];then
        service crond restart >/dev/null 2>&1
	else
		service cron restart >/dev/null 2>&1
	fi
    echo -e "${Info}成功关闭定时更新任务\n"
fi