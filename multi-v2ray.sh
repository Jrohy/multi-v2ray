#!/bin/bash
# Author: Jrohy
# github: https://github.com/Jrohy/multi-v2ray

#定时任务北京执行时间(0~23)
BEIJING_UPDATE_TIME=3

#记录最开始运行脚本的路径
BEGIN_PATH=$(pwd)

#安装方式, 0为全新安装, 1为保留v2ray配置更新
INSTALL_WAY=0

#定义操作变量, 0为否, 1为是
HELP=0

REMOVE=0

CHINESE=0

BASE_SOURCE_PATH="https://raw.githubusercontent.com/Jrohy/multi-v2ray/master"

CLEAN_IPTABLES_SHELL="$BASE_SOURCE_PATH/v2ray_util/global_setting/clean_iptables.sh"

BASH_COMPLETION_SHELL="$BASE_SOURCE_PATH/v2ray.bash"

UTIL_CFG="$BASE_SOURCE_PATH/v2ray_util/util_core/util.cfg"

UTIL_PATH="/etc/v2ray_util/util.cfg"

#Centos 临时取消别名
[[ -f /etc/redhat-release && -z $(echo $SHELL|grep zsh) ]] && unalias -a

[[ -z $(echo $SHELL|grep zsh) ]] && ENV_FILE=".bashrc" || ENV_FILE=".zshrc"

#######color code########
RED="31m"
GREEN="32m"
YELLOW="33m"
BLUE="36m"
FUCHSIA="35m"

colorEcho(){
    COLOR=$1
    echo -e "\033[${COLOR}${@:2}\033[0m"
}

#######get params#########
while [[ $# > 0 ]];do
    key="$1"
    case $key in
        --remove)
        REMOVE=1
        ;;
        -h|--help)
        HELP=1
        ;;
        -k|--keep)
        INSTALL_WAY=1
        colorEcho ${BLUE} "keep v2ray profile to update\n"
        ;;
        --zh)
        CHINESE=1
        colorEcho ${BLUE} "安装中文版..\n"
        ;;
        *)
                # unknown option
        ;;
    esac
    shift # past argument or value
done
#############################

help(){
    echo "bash multi-v2ray.sh [-h|--help] [-k|--keep] [--remove]"
    echo "  -h, --help           Show help"
    echo "  -k, --keep           keep the v2ray config.json to update"
    echo "      --remove         remove v2ray && multi-v2ray"
    echo "                       no params to new install"
    return 0
}

removeV2Ray() {
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

    #清理v2ray相关iptable规则
    bash <(curl -L -s $CLEAN_IPTABLES_SHELL)

    #卸载multi-v2ray
    pip uninstall v2ray_util -y
    rm -rf /etc/bash_completion.d/v2ray.bash >/dev/null 2>&1
    rm -rf /usr/local/bin/v2ray >/dev/null 2>&1
    rm -rf /etc/v2ray_util >/dev/null 2>&1

    #删除v2ray定时更新任务
    crontab -l|sed '/SHELL=/d;/v2ray/d' > crontab.txt
    crontab crontab.txt >/dev/null 2>&1
    rm -f crontab.txt >/dev/null 2>&1

    if [[ ${OS} == 'CentOS' || ${OS} == 'Fedora' ]];then
        service crond restart >/dev/null 2>&1
    else
        service cron restart >/dev/null 2>&1
    fi

    #删除multi-v2ray环境变量
    sed -i '/v2ray/d' ~/$ENV_FILE
    source ~/$ENV_FILE

    colorEcho ${GREEN} "uninstall success!"
}

closeSELinux() {
    #禁用SELinux
    if [ -s /etc/selinux/config ] && grep 'SELINUX=enforcing' /etc/selinux/config; then
        sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config
        setenforce 0
    fi
}

checkSys() {
    #检查是否为Root
    [ $(id -u) != "0" ] && { colorEcho ${RED} "Error: You must be root to run this script"; exit 1; }

    #检查系统信息
    if [[ -e /etc/redhat-release ]];then
        if [[ $(cat /etc/redhat-release | grep Fedora) ]];then
            OS='Fedora'
            PACKAGE_MANAGER='dnf'
        else
            OS='CentOS'
            PACKAGE_MANAGER='yum'
        fi
    elif [[ $(cat /etc/issue | grep Debian) ]];then
        OS='Debian'
        PACKAGE_MANAGER='apt-get'
    elif [[ $(cat /etc/issue | grep Ubuntu) ]];then
        OS='Ubuntu'
        PACKAGE_MANAGER='apt-get'
    elif [[ $(cat /etc/issue | grep Raspbian) ]];then
        OS='Raspbian'
        PACKAGE_MANAGER='apt-get'
    else
        colorEcho ${RED} "Not support OS, Please reinstall OS and retry!"
        exit 1
    fi
}

#安装依赖
installDependent(){
    if [[ ${OS} == 'CentOS' || ${OS} == 'Fedora' ]];then
        ${PACKAGE_MANAGER} install ntpdate socat crontabs lsof which -y
    else
        ${PACKAGE_MANAGER} update
        ${PACKAGE_MANAGER} install ntpdate socat cron lsof -y
    fi

    #install python3 & pip3
    bash <(curl -sL https://git.io/fhqMz)
}

#设置定时升级任务
planUpdate(){
    if [[ $CHINESE == 1 ]];then
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
        colorEcho ${BLUE} "beijing time ${BEIJING_UPDATE_TIME}, VPS time: ${LOCAL_TIME}\n"
    else
        LOCAL_TIME=3
    fi
    OLD_CRONTAB=$(crontab -l)
    echo "SHELL=/bin/bash" >> crontab.txt
    echo "${OLD_CRONTAB}" >> crontab.txt
	echo "0 ${LOCAL_TIME} * * * bash <(curl -L -s https://install.direct/go.sh) | tee -a /root/v2rayUpdate.log && service v2ray restart" >> crontab.txt
	crontab crontab.txt
	sleep 1
	if [[ ${OS} == 'CentOS' || ${OS} == 'Fedora' ]];then
        service crond restart
	else
		service cron restart
	fi
	rm -f crontab.txt
	colorEcho ${GREEN} "success open schedule update task: beijing time ${BEIJING_UPDATE_TIME}\n"
}

updateProject() {
    local DOMAIN=""

    [[ ! $(type pip3 2>/dev/null) ]] && colorEcho $RED "pip3 no install!" && exit 1

    if [[ -e /usr/local/multi-v2ray/multi-v2ray.conf ]];then
        TEMP_VALUE=$(cat /usr/local/multi-v2ray/multi-v2ray.conf|grep domain|awk 'NR==1')
        DOMAIN=${TEMP_VALUE/*=}
        rm -rf /usr/local/multi-v2ray
    fi

    pip3 install -U v2ray_util

    if [[ -e $UTIL_PATH ]];then
        [[ -z $(cat $UTIL_PATH|grep lang) ]] && echo "lang=en" >> $UTIL_PATH
    else
        mkdir -p /etc/v2ray_util
        curl $UTIL_CFG > $UTIL_PATH
        [[ ! -z $DOMAIN ]] && sed -i "s/^domain.*/domain=${DOMAIN}/g" $UTIL_PATH
    fi

    [[ $CHINESE == 1 ]] && sed -i "s/lang=en/lang=zh/g" $UTIL_PATH

    rm -f /usr/local/bin/v2ray >/dev/null 2>&1
    ln -s $(which v2ray-util) /usr/local/bin/v2ray

    #更新v2ray bash_completion脚本
    curl $BASH_COMPLETION_SHELL > /etc/bash_completion.d/v2ray.bash
    [[ -z $(echo $SHELL|grep zsh) ]] && source /etc/bash_completion.d/v2ray.bash
    
    #安装/更新V2ray主程序
    bash <(curl -L -s https://install.direct/go.sh)
}

#时间同步
timeSync() {
    if [[ ${INSTALL_WAY} == 0 ]];then
        echo -e "${Info} Time Synchronizing.. ${Font}"
        ntpdate pool.ntp.org
        if [[ $? -eq 0 ]];then 
            echo -e "${OK} Time Sync Success ${Font}"
            echo -e "${OK} now: `date -R`${Font}"
            sleep 1
        else
            echo -e "${Error} Time sync fail, please run command to sync:${Font}${Yellow}ntpdate pool.ntp.org${Font}"
        fi
    fi
}

profileInit() {

    #清理v2ray模块环境变量
    [[ $(grep v2ray ~/$ENV_FILE) ]] && sed -i '/v2ray/d' ~/$ENV_FILE && source ~/$ENV_FILE

    #解决Python3中文显示问题
    [[ -z $(grep PYTHONIOENCODING=utf-8 ~/$ENV_FILE) ]] && echo "export PYTHONIOENCODING=utf-8" >> ~/$ENV_FILE && source ~/$ENV_FILE

    # 加入v2ray tab补全环境变量
    [[ -z $(echo $SHELL|grep zsh) && -z $(grep v2ray.bash ~/$ENV_FILE) ]] && echo "source /etc/bash_completion.d/v2ray.bash" >> ~/$ENV_FILE && source ~/$ENV_FILE

    #全新安装的新配置
    if [[ ${INSTALL_WAY} == 0 ]];then 
        v2ray new
    else
        v2ray convert
    fi

    bash <(curl -L -s $CLEAN_IPTABLES_SHELL)
    echo ""
}

installFinish() {
    #回到原点
    cd ${BEGIN_PATH}

    [[ ${INSTALL_WAY} == 0 ]] && WAY="install" || WAY="update"
    colorEcho  ${GREEN} "multi-v2ray ${WAY} success!\n"

    clear

    v2ray info

    echo -e "please input 'v2ray' command to manage v2ray\n"
}


main() {

    [[ ${HELP} == 1 ]] && help && return

    [[ ${REMOVE} == 1 ]] && removeV2Ray && return

    [[ ${INSTALL_WAY} == 0 ]] && colorEcho ${BLUE} "new install\n"

    checkSys

    installDependent

    closeSELinux

    timeSync

    #设置定时任务
    [[ -z $(crontab -l|grep v2ray) ]] && planUpdate

    updateProject

    profileInit

    service v2ray restart

    installFinish
}

main