#!/bin/bash
# Author: Jrohy
# github: https://github.com/Jrohy/multi-v2ray

#定时任务北京执行时间(0~23)
BEIJING_UPDATE_TIME=3

#记录最开始运行脚本的路径
BEGIN_PATH=$(pwd)

#安装方式0: 全新安装, 1:保留配置更新 , 2:仅更新multi-v2ray源码
INSTARLL_WAY="0"

DEV_MODE=""

HELP=""

REMOVE=""

#######color code########
RED="31m"      # Error message
GREEN="32m"    # Success message
YELLOW="33m"   # Warning message
BLUE="36m"     # Info message

colorEcho(){
    COLOR=$1
    echo -e "\033[${COLOR}${@:2}\033[0m"
}

#######get params#########
while [[ $# > 0 ]];do
    key="$1"
    case $key in
        --remove)
        REMOVE="1"
        ;;
        -h|--help)
        HELP="1"
        ;;
        -k|--keep)
        INSTARLL_WAY="1"
        colorEcho ${BLUE} "当前以keep保留配置文件形式更新, 若失败请用全新安装\n"
        ;;
        -c|--code)
        INSTARLL_WAY="2"
        colorEcho ${BLUE} "当前仅更新multi-v2ray源码\n"
        ;;
        -d|--dev)
        DEV_MODE="1"
        colorEcho ${BLUE} "当前为开发模式, 用dev分支来更新\n"
        ;;
        *)
                # unknown option
        ;;
    esac
    shift # past argument or value
done
#############################

help(){
    echo "source multi-v2ray.sh [-h|--help] [-k|--keep] [-d|--dev][-c|--code][--remove]"
    echo "  -h, --help           Show help"
    echo "  -k, --keep           keep the v2ray config.json to update"
    echo "  -d, --dev            update from dev branch"
    echo "  -c, --code           only update multi-v2ray code"
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

    #卸载multi-v2ray
    rm -rf /usr/local/multi-v2ray >/dev/null 2>&1
    rm -rf /usr/local/bin/v2ray >/dev/null 2>&1

    #删除v2ray定时更新任务
    crontab -l|sed '/SHELL=/d;/v2ray/d' > crontab.txt
    crontab crontab.txt >/dev/null 2>&1
    rm -f crontab.txt >/dev/null 2>&1

    if [[ "${OS}" == "CentOS" ]];then
        service crond restart >/dev/null 2>&1
    else
        service cron restart >/dev/null 2>&1
    fi

    #删除multi-v2ray环境变量
    sed -i '/v2ray/d' ~/.bashrc
    source ~/.bashrc

    colorEcho ${GREEN} "卸载完成！"
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
}

#安装依赖
installDependent(){
    if [[ ${OS} == 'CentOS' ]];then
        yum install epel-release curl wget unzip git ntp ntpdate socat crontabs lsof -y
        [[ -z $(rpm -qa|grep python3) ]] && yum install python34 -y
    else
        apt-get update
        apt-get install curl unzip git ntp wget ntpdate socat cron lsof -y
        [[ -z $(dpkg -l|grep python3) ]] && apt-get install python3 -y
    fi

    # 安装 pip依赖
    python3 <(curl -sL https://bootstrap.pypa.io/get-pip.py)
    pip3 install pyopenssl
}

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

updateProject() {
    [[ "${INSTARLL_WAY}" != "0" ]] && mv /usr/local/multi-v2ray/my_domain ~ &>/dev/null
    cd /usr/local/
    #v2ray.fun目录存在的情况
    [[ -e v2ray.fun ]] && mv v2ray.fun/my_domain ~ && rm -rf v2ray.fun
    
    if [[ -e multi-v2ray && -e multi-v2ray/.git ]];then
        cd multi-v2ray

        if [[ "$DEV_MODE" == "1" ]];then
            git checkout dev
        else 
            git checkout master
        fi

        git reset --hard && git pull
    else
        [[ "$DEV_MODE" == "1" ]] && BRANCH="dev" || BRANCH="master" 
        git clone -b $BRANCH https://github.com/Jrohy/multi-v2ray
    fi
    [[ "${INSTARLL_WAY}" != "0" ]] && mv -f ~/my_domain .

    #更新v2ray bash_completion脚本
    cp -f /usr/local/multi-v2ray/v2ray.bash /etc/bash_completion.d/
    source /etc/bash_completion.d/v2ray.bash
    
    #安装/更新V2ray主程序
    bash <(curl -L -s https://install.direct/go.sh)
}

#时间同步
timeSync() {
    if [[ "${INSTARLL_WAY}" == "0" ]];then
        systemctl stop ntp &>/dev/null
        echo -e "${Info} 正在进行时间同步 ${Font}"
        ntpdate time.nist.gov
        if [[ $? -eq 0 ]];then 
            echo -e "${OK} 时间同步成功 ${Font}"
            echo -e "${OK} 当前系统时间 `date -R`${Font}"
            sleep 1
        else
            echo -e "${Error} 时间同步失败，可以手动执行命令同步:${Font}${Yellow}ntpdate time.nist.gov${Font}"
        fi
    fi
}


profileInit() {
    #配置V2ray初始环境
    cp /usr/local/multi-v2ray/v2ray /usr/local/bin
    chmod +x /usr/local/bin/v2ray

    #加入multi-v2ray模块搜索路径
    [[ -z $(grep multi-v2ray ~/.bashrc) ]] && echo "export PYTHONPATH=$PYTHONPATH:/usr/local/multi-v2ray" >> ~/.bashrc && source ~/.bashrc

    # 加入v2ray tab补全环境变量
    [[ -z $(grep v2ray.bash ~/.bashrc) ]] && echo "source /etc/bash_completion.d/v2ray.bash" >> ~/.bashrc && source ~/.bashrc

    #解决Python3中文显示问题
    [[ -z $(grep PYTHONIOENCODING=utf-8 ~/.bashrc) ]] && echo "export PYTHONIOENCODING=utf-8" >> ~/.bashrc && source ~/.bashrc

    #全新安装的新配置
    if [[ "${INSTARLL_WAY}" == "0" ]];then 
        rm -rf /etc/v2ray/config.json
        cp /usr/local/multi-v2ray/json_template/server.json /etc/v2ray/config.json

        #产生随机uuid
        UUID=$(cat /proc/sys/kernel/random/uuid)
        sed -i "s/cc4f8d5b-967b-4557-a4b6-bde92965bc27/${UUID}/g" /etc/v2ray/config.json

        #产生随机端口
        D_PORT=$(shuf -i 1000-65535 -n 1)
        sed -i "s/999999999/${D_PORT}/g" /etc/v2ray/config.json

        #产生默认配置mkcp+随机3种伪装类型type
        python3 /usr/local/multi-v2ray/base_util/random_stream.py
        python3 -c "from config_modify import stream; StreamModifier().random_kcp();"

        python3 /usr/local/multi-v2ray/client.py
        python3 -c "from utils import open_port; open_port();"
    fi
}

installFinish() {
    #回到原点
    cd ${BEGIN_PATH}

    [[ ${INSTARLL_WAY} == "0" ]] && way="安装" || way="更新"
    colorEcho  ${GREEN} "multi-v2ray ${way}成功！\n"

    clear

    echo "V2ray配置信息:"
    #安装完后显示v2ray的配置信息，用于快速部署
    python3 -c "from loader import Loader; print(loader.profile);"

    echo -e "输入 v2ray 回车即可进行服务管理\n"
}


main() {

    [[ ${HELP} == "1" ]] && help && return

    [[ ${REMOVE} == "1" ]] && removeV2Ray && return

    [[ ${INSTARLL_WAY} == "0" ]] && colorEcho ${BLUE} "当前为全新安装\n"

    if [[ ${INSTARLL_WAY} != "2" ]];then 
        checkSys

        installDependent

        closeSELinux

        timeSync

        #设置定时任务
        [[ -z $(crontab -l|grep v2ray) ]] && planUpdate

    fi

    updateProject

    profileInit

    service v2ray restart

    installFinish
}

main