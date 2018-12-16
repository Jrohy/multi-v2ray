#!/bin/bash
clean_old_iptables(){
    local TYPE=$1
    RESULT=$(iptables -nvL $TYPE --line-number|grep state|awk -F ':' '{print $2"  " $1}'|awk '{print $2" "$1}'|sort -n -k1 -r)
    echo "$RESULT" | while read LINE
    do
        LINE_ARRAY=($LINE)
        if [[ ${LINE_ARRAY[1]} && $(lsof -i:${LINE_ARRAY[1]}|grep v2ray) ]];then
            iptables -D $TYPE ${LINE_ARRAY[0]}
        fi
    done
}

clean_iptables(){
    local TYPE=$1
    RESULT=$(iptables -nvL $TYPE --line-number|grep :|awk -F ':' '{print $2"  " $1}'|awk '{print $2" "$1}'|sort -n -k1 -r)
    echo "$RESULT" | while read LINE
    do
        LINE_ARRAY=($LINE)
        [[ ${LINE_ARRAY[1]} && -z $(lsof -i:${LINE_ARRAY[1]}) ]] && iptables -D $TYPE ${LINE_ARRAY[0]}
    done
}

clean_old_iptables INPUT
clean_iptables INPUT
clean_iptables OUTPUT