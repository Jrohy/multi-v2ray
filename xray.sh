#!/bin/bash
# Author: Jrohy
# github: https://github.com/Jrohy/multi-xray

#定时任务北京执行时间(0~23)
BEIJING_UPDATE_TIME=3

#记录最开始运行脚本的路径
BEGIN_PATH=$(pwd)

#安装方式, 0为全新安装, 1为保留xray配置更新
INSTALL_WAY=0

#定义操作变量, 0为否, 1为是
HELP=0

REMOVE=0

CHINESE=0

BASE_SOURCE_PATH="https://multi.netlify.app"

UTIL_PATH="/etc/xray_util/util.cfg"

UTIL_CFG="$BASE_SOURCE_PATH/xray_util/util_core/util.cfg"

BASH_COMPLETION_SHELL="$BASE_SOURCE_PATH/xray"

CLEAN_IPTABLES_SHELL="$BASE_SOURCE_PATH/xray_util/global_setting/clean_iptables.sh"

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
        colorEcho ${BLUE} "keep config to update\n"
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
    echo "bash xray.sh [-h|--help] [-k|--keep] [--remove]"
    echo "  -h, --help           Show help"
    echo "  -k, --keep           keep the config.json to update"
    echo "      --remove         remove xray,xray && multi-xray"
    echo "                       no params to new install"
    return 0
}

removexray() {
    #卸载xray脚本
    bash <(curl -L -s https://multi.netlify.app/go.sh) --remove >/dev/null 2>&1
    rm -rf /etc/xray >/dev/null 2>&1
    rm -rf /var/log/xray >/dev/null 2>&1

    #卸载Xray脚本
    bash <(curl -L -s https://multi.netlify.app/go.sh) --remove -x >/dev/null 2>&1
    rm -rf /etc/xray >/dev/null 2>&1
    rm -rf /var/log/xray >/dev/null 2>&1

    #清理xray相关iptable规则
    bash <(curl -L -s $CLEAN_IPTABLES_SHELL)

    #卸载multi-xray
    pip uninstall xray_util -y
    rm -rf /usr/share/bash-completion/completions/xray.bash >/dev/null 2>&1
    rm -rf /usr/share/bash-completion/completions/xray >/dev/null 2>&1
    rm -rf /usr/share/bash-completion/completions/xray >/dev/null 2>&1
    rm -rf /etc/bash_completion.d/xray.bash >/dev/null 2>&1
    rm -rf /usr/local/bin/xray >/dev/null 2>&1
    rm -rf /etc/xray_util >/dev/null 2>&1
    rm -rf /etc/profile.d/iptables.sh >/dev/null 2>&1
    rm -rf /root/.iptables >/dev/null 2>&1

    #删除xray定时更新任务
    crontab -l|sed '/SHELL=/d;/xray/d'|sed '/SHELL=/d;/xray/d' > crontab.txt
    crontab crontab.txt >/dev/null 2>&1
    rm -f crontab.txt >/dev/null 2>&1

    if [[ ${PACKAGE_MANAGER} == 'dnf' || ${PACKAGE_MANAGER} == 'yum' ]];then
        systemctl restart crond >/dev/null 2>&1
    else
        systemctl restart cron >/dev/null 2>&1
    fi

    #删除multi-xray环境变量
    sed -i '/xray/d' ~/$ENV_FILE
    sed -i '/xray/d' ~/$ENV_FILE
    source ~/$ENV_FILE

    RC_SERVICE=`systemctl status rc-local|grep loaded|egrep -o "[A-Za-z/]+/rc-local.service"`

    RC_FILE=`cat $RC_SERVICE|grep ExecStart|awk '{print $1}'|cut -d = -f2`

    sed -i '/iptables/d' ~/$RC_FILE

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

    if [[ `command -v apt-get` ]];then
        PACKAGE_MANAGER='apt-get'
    elif [[ `command -v dnf` ]];then
        PACKAGE_MANAGER='dnf'
    elif [[ `command -v yum` ]];then
        PACKAGE_MANAGER='yum'
    else
        colorEcho $RED "Not support OS!"
        exit 1
    fi
}

#安装依赖
installDependent(){
    if [[ ${PACKAGE_MANAGER} == 'dnf' || ${PACKAGE_MANAGER} == 'yum' ]];then
        ${PACKAGE_MANAGER} install socat crontabs bash-completion which -y
    else
        ${PACKAGE_MANAGER} update
        ${PACKAGE_MANAGER} install socat cron bash-completion ntpdate gawk -y
    fi

    #install python3 & pip
    source <(curl -sL https://python3.netlify.app/install.sh)
}

updateProject() {
    [[ ! $(type pip 2>/dev/null) ]] && colorEcho $RED "pip no install!" && exit 1

    [[ -e /etc/profile.d/iptables.sh ]] && rm -f /etc/profile.d/iptables.sh

    RC_SERVICE=`systemctl status rc-local|grep loaded|egrep -o "[A-Za-z/]+/rc-local.service"`

    RC_FILE=`cat $RC_SERVICE|grep ExecStart|awk '{print $1}'|cut -d = -f2`

    if [[ ! -e $RC_FILE || -z `cat $RC_FILE|grep iptables` ]];then
        LOCAL_IP=`curl -s http://api.ipify.org 2>/dev/null`
        [[ `echo $LOCAL_IP|grep :` ]] && IPTABLE_WAY="ip6tables" || IPTABLE_WAY="iptables" 
        if [[ ! -e $RC_FILE || -z `cat $RC_FILE|grep "/bin/bash"` ]];then
            echo "#!/bin/bash" >> $RC_FILE
        fi
        if [[ -z `cat $RC_SERVICE|grep "\[Install\]"` ]];then
            cat >> $RC_SERVICE << EOF

[Install]
WantedBy=multi-user.target
EOF
            systemctl daemon-reload
        fi
        echo "[[ -e /root/.iptables ]] && $IPTABLE_WAY-restore -c < /root/.iptables" >> $RC_FILE
        chmod +x $RC_FILE
        systemctl restart rc-local
        systemctl enable rc-local

        $IPTABLE_WAY-save -c > /root/.iptables
    fi

    pip install -U xray_util

    if [[ -e $UTIL_PATH ]];then
        [[ -z $(cat $UTIL_PATH|grep lang) ]] && echo "lang=en" >> $UTIL_PATH
    else
        mkdir -p /etc/xray_util
        curl $UTIL_CFG > $UTIL_PATH
    fi

    [[ $CHINESE == 1 ]] && sed -i "s/lang=en/lang=zh/g" $UTIL_PATH

    rm -f /usr/local/bin/xray >/dev/null 2>&1
    ln -s $(which xray-util) /usr/local/bin/xray
    rm -f /usr/local/bin/xray >/dev/null 2>&1
    ln -s $(which xray-util) /usr/local/bin/xray

    #移除旧的xray bash_completion脚本
    [[ -e /etc/bash_completion.d/xray.bash ]] && rm -f /etc/bash_completion.d/xray.bash
    [[ -e /usr/share/bash-completion/completions/xray.bash ]] && rm -f /usr/share/bash-completion/completions/xray.bash

    #更新xray bash_completion脚本
    curl $BASH_COMPLETION_SHELL > /usr/share/bash-completion/completions/xray
    curl $BASH_COMPLETION_SHELL > /usr/share/bash-completion/completions/xray
    if [[ -z $(echo $SHELL|grep zsh) ]];then
        source /usr/share/bash-completion/completions/xray
        source /usr/share/bash-completion/completions/xray
    fi
    
    #安装Xray主程序
    [[ ${INSTALL_WAY} == 0 ]] && bash <(curl -L -s https://multi.netlify.app/go.sh) --xray
}

#时间同步
timeSync() {
    if [[ ${INSTALL_WAY} == 0 ]];then
        echo -e "${Info} Time Synchronizing.. ${Font}"
        if [[ `command -v ntpdate` ]];then
            ntpdate pool.ntp.org
        elif [[ `command -v chronyc` ]];then
            chronyc -a makestep
        fi

        if [[ $? -eq 0 ]];then 
            echo -e "${OK} Time Sync Success ${Font}"
            echo -e "${OK} now: `date -R`${Font}"
        fi
    fi
}

profileInit() {

    #清理xray模块环境变量
    [[ $(grep xray ~/$ENV_FILE) ]] && sed -i '/xray/d' ~/$ENV_FILE && source ~/$ENV_FILE

    #解决Python3中文显示问题
    [[ -z $(grep PYTHONIOENCODING=utf-8 ~/$ENV_FILE) ]] && echo "export PYTHONIOENCODING=utf-8" >> ~/$ENV_FILE && source ~/$ENV_FILE

    #全新安装的新配置
    [[ ${INSTALL_WAY} == 0 ]] && xray new

    echo ""
}

installFinish() {
    #回到原点
    cd ${BEGIN_PATH}

    [[ ${INSTALL_WAY} == 0 ]] && WAY="install" || WAY="update"
    colorEcho  ${GREEN} "multi-xray ${WAY} success!\n"

    if [[ ${INSTALL_WAY} == 0 ]]; then
        clear

        xray info

        echo -e "please input 'xray' command to manage xray\n"
    fi
}


main() {

    [[ ${HELP} == 1 ]] && help && return

    [[ ${REMOVE} == 1 ]] && removexray && return

    [[ ${INSTALL_WAY} == 0 ]] && colorEcho ${BLUE} "new install\n"

    checkSys

    installDependent

    closeSELinux

    timeSync

    updateProject

    profileInit

    installFinish
}

main