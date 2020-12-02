#!/bin/bash
PORT=$1

NETWORK=$2

[[ $# == 0 ]]  && exit 1 

clean_traffic(){
    local TYPE=$1
    if [[ $NETWORK ]];then
        RESULT=$(ip6tables -nvL $TYPE --line-numbers 2>/dev/null|grep -w "$PORT"|awk '{print $1}')
    else
        RESULT=$(iptables -nvL $TYPE --line-numbers 2>/dev/null|grep -w "$PORT"|awk '{print $1}')
    fi
    echo "$RESULT" | while read LINE
    do
        if [[ ${LINE}  ]];then
            [[ $NETWORK ]] && ip6tables -Z $TYPE $LINE || iptables -Z $TYPE $LINE
        fi
    done
}

clean_traffic INPUT
clean_traffic OUTPUT