#!/bin/bash
# Author: Jrohy
# github: https://github.com/Jrohy/multi-v2ray

#定时任务北京执行时间(0~23)
BEIJING_UPDATE_TIME=3

#记录最开始运行脚本的路径
BEGIN_PATH=$(pwd)

#安装方式0: 全新安装, 1:保留配置更新 , 2:仅更新multi-v2ray源码
INSTARLL_WAY=0

#定义操作变量, 0为否, 1为是
HELP=0

REMOVE=0

FORCE=0

IS_LATEST=0

UPDATE_VERSION=""

APP_PATH="/usr/local/multi-v2ray"

#Centos 临时取消别名
[[ -f /etc/redhat-release && -z $(echo $SHELL|grep zsh) ]] && unalias -a

[[ -z $(echo $SHELL|grep zsh) ]] && ENV_FILE=".bashrc" || ENV_FILE=".zshrc"

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
        REMOVE=1
        ;;
        -h|--help)
        HELP=1
        ;;
        -f|--force)
        FORCE=1
        ;;
        -v|--version)
        UPDATE_VERSION="$2"
        echo -e "更新multi-v2ray到 $(colorEcho ${BLUE} $UPDATE_VERSION) 版本\n"
        shift
        ;;
        -k|--keep)
        INSTARLL_WAY=1
        colorEcho ${BLUE} "当前以keep保留配置文件形式更新, 若失败请用全新安装\n"
        ;;
        -c|--code)
        INSTARLL_WAY=2
        colorEcho ${BLUE} "当前仅更新multi-v2ray源码\n"
        ;;
        *)
                # unknown option
        ;;
    esac
    shift # past argument or value
done
#############################

checkUpdate(){
    LASTEST_VERSION=$(curl -H 'Cache-Control: no-cache' -s "https://api.github.com/repos/Jrohy/multi-v2ray/releases/latest" | grep 'tag_name' | cut -d\" -f4)

    if [[ -e /usr/local/bin/v2ray ]];then
        VERSION_TEMP_VALUE=$(cat /usr/local/bin/v2ray|grep SHELL_V2RAY|awk 'NR==1'|sed 's/\"//g')
        if [[ ! -z $VERSION_TEMP_VALUE ]]; then
            CURRENT_VERSION=${VERSION_TEMP_VALUE/*=}
            if [[ ! -z $UPDATE_VERSION && $UPDATE_VERSION == $CURRENT_VERSION ]];then
                echo -e "multi-v2ray当前版本: $(colorEcho $GREEN $CURRENT_VERSION), 已是指定版本!!!"
                IS_LATEST=1
                return
            fi
            if [[ -z $UPDATE_VERSION && $FORCE == 0 && $INSTARLL_WAY != 0 && $LASTEST_VERSION == $CURRENT_VERSION ]]; then
                echo -e "multi-v2ray当前版本: $(colorEcho $GREEN $CURRENT_VERSION), 已是最新!!!"
                IS_LATEST=1
                return
            fi
        fi
    fi

    [[ -z $UPDATE_VERSION ]] && UPDATE_VERSION=$LASTEST_VERSION
}

help(){
    echo "source multi-v2ray.sh [-h|--help] [-k|--keep] [-c|--code] [-f|--force] [--remove]"
    echo "  -h, --help           Show help"
    echo "  -k, --keep           keep the v2ray config.json to update"
    echo "  -c, --code           only update multi-v2ray code"
    echo "  -f, --force          force to update multi-v2ray lastest code"
    echo "  -v, --version        update multi-v2ray to special version"
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
    rm -rf $APP_PATH >/dev/null 2>&1
    rm -rf /etc/bash_completion.d/v2ray.bash >/dev/null 2>&1
    rm -rf /usr/local/bin/v2ray >/dev/null 2>&1

    #删除v2ray定时更新任务
    crontab -l|sed '/SHELL=/d;/v2ray/d' > crontab.txt
    crontab crontab.txt >/dev/null 2>&1
    rm -f crontab.txt >/dev/null 2>&1

    if [[ ${OS} == "CentOS" ]];then
        service crond restart >/dev/null 2>&1
    else
        service cron restart >/dev/null 2>&1
    fi

    #删除multi-v2ray环境变量
    sed -i '/v2ray/d' ~/$ENV_FILE
    source ~/$ENV_FILE

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
        if [[ -z $(rpm -qa|grep python3) ]];then
            yum install https://centos7.iuscommunity.org/ius-release.rpm -y
            yum install python36u -y
            ln -s /bin/python3.6 /bin/python3
        fi
    else
        apt-get update
        apt-get install curl unzip git ntp wget ntpdate socat cron lsof -y
        [[ -z $(dpkg -l|grep python3) ]] && apt-get install python3 -y
        apt-get install python3-distutils -y
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
	if [[ ${OS} == "CentOS" ]];then
        service crond restart
	else
		service cron restart
	fi
	rm -f crontab.txt
	colorEcho ${GREEN} "成功配置每天北京时间${BEIJING_UPDATE_TIME}点自动升级V2ray内核任务\n"
}

updateProject() {
    local DOMAIN=""

    if [[ -e $APP_PATH/my_domain ]];then
        DOMAIN=$(cat $APP_PATH/my_domain|awk 'NR==1')
    elif [[ -e $APP_PATH/multi-v2ray.conf ]];then
        TEMP_VALUE=$(cat $APP_PATH/multi-v2ray.conf|grep domain|awk 'NR==1')
        DOMAIN=${TEMP_VALUE/*=}
    fi

    cd /usr/local/
    if [[ -e multi-v2ray && -e multi-v2ray/.git ]];then
        cd multi-v2ray

        FIR_COMMIT_AUTHOR=$(git log --reverse | awk 'NR==2'| awk '{print $2}')
        if [[ $FIR_COMMIT_AUTHOR == 'Jrohy' ]];then
            git reset --hard HEAD && git clean -d -f
            if [[ $FORCE == 1 ]]; then
                git pull origin master
            else
                git fetch origin && git checkout $UPDATE_VERSION
            fi
        else
            cd /usr/local/
            rm -rf multi-v2ray
            git clone https://github.com/Jrohy/multi-v2ray
        fi
    else
        git clone https://github.com/Jrohy/multi-v2ray
    fi

    [[ ! -z $DOMAIN ]] && sed -i "s/^domain.*/domain=${DOMAIN}/g" $APP_PATH/multi-v2ray.conf

    #更新v2ray bash_completion脚本
    cp -f $APP_PATH/v2ray.bash /etc/bash_completion.d/
    [[ -z $(echo $SHELL|grep zsh) ]] && source /etc/bash_completion.d/v2ray.bash
    
    #安装/更新V2ray主程序
    [[ ${INSTARLL_WAY} != 2 ]] && bash <(curl -L -s https://install.direct/go.sh)
}

#时间同步
timeSync() {
    if [[ ${INSTARLL_WAY} == 0 ]];then
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
    rm -f /usr/local/bin/v2ray >/dev/null 2>&1
    #配置V2ray初始环境
    cp -f $APP_PATH/v2ray /usr/local/bin
    chmod +x /usr/local/bin/v2ray

    #加入multi-v2ray模块搜索路径
    [[ -z $(grep multi-v2ray ~/$ENV_FILE) ]] && echo "export PYTHONPATH=$PYTHONPATH:$APP_PATH" >> ~/$ENV_FILE && source ~/$ENV_FILE

    # 加入v2ray tab补全环境变量
    [[ -z $(echo $SHELL|grep zsh) && -z $(grep v2ray.bash ~/$ENV_FILE) ]] && echo "source /etc/bash_completion.d/v2ray.bash" >> ~/$ENV_FILE && source ~/$ENV_FILE

    #解决Python3中文显示问题
    [[ -z $(grep PYTHONIOENCODING=utf-8 ~/$ENV_FILE) ]] && echo "export PYTHONIOENCODING=utf-8" >> ~/$ENV_FILE && source ~/$ENV_FILE

    #全新安装的新配置
    if [[ ${INSTARLL_WAY} == 0 ]];then 
        rm -rf /etc/v2ray/config.json
        cp $APP_PATH/json_template/server.json /etc/v2ray/config.json

        #产生随机uuid
        UUID=$(cat /proc/sys/kernel/random/uuid)
        sed -i "s/cc4f8d5b-967b-4557-a4b6-bde92965bc27/${UUID}/g" /etc/v2ray/config.json

        #产生随机端口
        D_PORT=$(shuf -i 1000-65535 -n 1)
        sed -i "s/999999999/${D_PORT}/g" /etc/v2ray/config.json

        #产生默认配置mkcp+随机3种伪装类型type
        python3 -c "from config_modify import stream; stream.StreamModifier().random_kcp();"
        python3 $APP_PATH/client.py
    else
        python3 $APP_PATH/converter.py
    fi

    bash $APP_PATH/global_setting/clean_iptables.sh
    echo ""
    echo -e "生成 $(colorEcho $BLUE iptables) 流量统计规则中.."
    python3 -c "from utils import open_port; open_port();"
}

installFinish() {
    #回到原点
    cd ${BEGIN_PATH}

    [[ ${INSTARLL_WAY} == 0 ]] && WAY="安装" || WAY="更新"
    colorEcho  ${GREEN} "multi-v2ray ${WAY}成功！\n"

    clear

    echo "V2ray配置信息:"
    #安装完后显示v2ray的配置信息，用于快速部署
    python3 -c "from loader import Loader; print(Loader().profile);"

    echo -e "输入 v2ray 回车即可进行服务管理\n"
}


main() {

    [[ ${HELP} == 1 ]] && help && return

    [[ ${REMOVE} == 1 ]] && removeV2Ray && return

    [[ ${FORCE} == 1 ]] && colorEcho ${BLUE} "当前为强制更新模式, 会更新到master最新代码\n"

    checkUpdate && [[ $IS_LATEST == 1 ]] && return

    [[ ${INSTARLL_WAY} == 0 ]] && colorEcho ${BLUE} "当前为全新安装\n"

    if [[ ${INSTARLL_WAY} != 2 ]];then 
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