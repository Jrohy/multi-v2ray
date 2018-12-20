#!/bin/bash
PORT=$1

[[ $# == 0 ]]  && exit 1 

clean_traffic(){
    local TYPE=$1
    RESULT=$(iptables -nvL $TYPE --line-numbers|grep -w "$PORT"|awk '{print $1}')
    echo "$RESULT" | while read LINE
    do
        [[ ${LINE}  ]] && iptables -Z $TYPE $LINE
    done
}

clean_traffic INPUT
clean_traffic OUTPUT