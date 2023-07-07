#!/bin/bash

uptime=`cat /proc/uptime |awk '{print $1}'`
if [[ `echo "$uptime < 100"|bc` -eq 1 ]];then
    local_ip=`curl -s http://api.ipify.org 2>/dev/null`
    if [[ -e /root/.iptables ]];then
        [[ `echo $local_ip|grep :` ]] && iptable_way="ip6tables" || iptable_way="iptables" 
        $iptable_way-restore -c < /root/.iptables
    fi
fi

if [[ ! -e /etc/v2ray ]];then
    mkdir /etc/v2ray
    v2ray new >/dev/null 2>&1
fi

touch /.run.log
/usr/bin/v2ray/v2ray run -c /etc/v2ray/config.json > /.run.log &

tail -f /.run.log
