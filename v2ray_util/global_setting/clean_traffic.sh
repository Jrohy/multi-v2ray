#!/bin/bash
port=$1

network=$2

[[ $# == 0 ]]  && exit 1 

clean_traffic(){
    local type=$1
    if [[ $network ]];then
        result=$(ip6tables -nvL $type --line-numbers 2>/dev/null|grep -w "$port"|awk '{print $1}')
    else
        result=$(iptables -nvL $type --line-numbers 2>/dev/null|grep -w "$port"|awk '{print $1}')
    fi
    echo "$result" | while read line
    do
        if [[ ${line}  ]];then
            [[ $network ]] && ip6tables -Z $type $line || iptables -Z $type $line
        fi
    done
}

clean_traffic INPUT
clean_traffic OUTPUT
