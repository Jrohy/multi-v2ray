#!/bin/bash

#定时任务北京执行时间(0~23)
BEIJING_UPDATE_TIME=3

#######color code########
RED="31m"      # Error message
GREEN="32m"    # Success message
YELLOW="33m"   # Warning message
BLUE="36m"     # Info message

##########################
colorEcho(){
    COLOR=$1
    echo -e "\033[${COLOR}${@:2}\033[0m"
}

#检查是否为Root
[ $(id -u) != "0" ] && { colorEcho ${RED} "Error: You must be root to run this script"; exit 1; }

#检查系统信息
if [ -f /etc/redhat-release ];then
        OS='CentOS'
    elif [ ! -z "`cat /etc/issue | grep bian`" ];then
        OS='Debian'
    elif [ ! -z "`cat /etc/issue | grep Ubuntu`" ];then
        OS='Ubuntu'
    else
        colorEcho ${RED} "Not support OS, Please reinstall OS and retry!"
        exit 1
fi

#设置定时升级任务
planUpdate(){
    #计算北京时间早上3点时VPS的实际时间
    ORIGIN_TIME_ZONE=$(date -R|awk '{printf"%d",$6}')
    LOCAL_TIME_ZONE=${ORIGIN_TIME_ZONE%00}
    BEIJING_ZONE=8
    DIFF_ZONE=$[$BEIJING_ZONE-$LOCAL_TIME_ZONE]
    LOCAL_TIME=$[$BEIJING_UPDATE_TIME-$DIFF_ZONE]
    if [ $LOCAL_TIME -lt 0 ];then
        LOCAL_TIME=$[24+$LOCAL_TIME]
    elif [ $LOCAL_TIME -ge 24 ];then
        LOCAL_TIME=$[$LOCAL_TIME-24]
    fi
	colorEcho ${BLUE} "北京时间${BEIJING_UPDATE_TIME}点，VPS时间为${LOCAL_TIME}点\n"

    OLD_CRONTAB=$(crontab -l)
    echo "SHELL=/bin/bash" >> crontab.txt
    echo "${OLD_CRONTAB}" >> crontab.txt
	echo "0 ${LOCAL_TIME} * * * bash <(curl -L -s https://install.direct/go.sh) | tee -a /root/v2rayUpdate.log && service v2ray restart" >> crontab.txt
	crontab crontab.txt
	sleep 1
	if [[ "${OS}" == "CentOS" ]];then
        service crond restart
	else
		service cron restart
	fi
	rm -f crontab.txt
	colorEcho ${GREEN} "成功配置每天北京时间${BEIJING_UPDATE_TIME}点自动升级V2ray内核任务\n"
}

[[ -z $(crontab -l|grep v2ray) ]] && IS_OPEN="关闭" || IS_OPEN="开启"

echo -e "当前定时更新任务状态: ${IS_OPEN}\n" 

echo -e ""
echo -e "1.开启定时更新任务\n"
echo -e "2.关闭定时更新任务\n"
echo -e "Tip: 开启定时更新v2ray的更新时间为每天北京时间3:00更新"

while :; do echo
    read -n1 -p "请选择： " CHOICE
    if [[ ! $CHOICE =~ ^[1-2]$ ]]; then
        if [[ -z ${CHOICE} ]];then
            bash /usr/local/bin/v2ray
            exit 0
        fi
        colorEcho ${RED} "输入错误! 请输入正确的数字!"
    else
        echo -e "\n"
        break
    fi
done

if [[ ${CHOICE} == 1 ]]; then
    if [[ ${IS_OPEN} == "开启" ]]; then
        colorEcho ${YELLOW} "当前定时更新已开启,无需重复操作!\n"
        bash /usr/local/bin/v2ray
        exit 0
    fi
    #设置定时任务
    planUpdate
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
    colorEcho ${GREEN} "成功关闭定时更新任务\n"
fi