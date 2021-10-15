#!/bin/bash

UPTIME=`cat /proc/uptime |awk '{print $1}'`
if [[ `echo "$UPTIME < 100"|bc` -eq 1 ]];then
    LOCAL_IP=`curl -s http://api.ipify.org 2>/dev/null`
    if [[ -e /root/.iptables ]];then
        [[ `echo $LOCAL_IP|grep :` ]] && IPTABLE_WAY="ip6tables" || IPTABLE_WAY="iptables" 
        $IPTABLE_WAY-restore -c < /root/.iptables
    fi
fi

if [[ ! -e /etc/xray ]];then
    mkdir /etc/xray
    xray new >/dev/null 2>&1
fi

touch /.run.log
/usr/bin/xray/xray -config=/etc/xray/config.json > /.run.log &

tail -f /.run.log