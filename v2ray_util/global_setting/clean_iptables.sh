#!/bin/bash
clean_iptables(){
    local TYPE=$1
    if [[ $NETWORK == 1 ]];then
        RESULT=$(ip6tables -nvL $TYPE --line-number 2>/dev/null|grep :|awk '{printf "%s %s\n",$1,$NF}'|sed 's/dpt://g'|sed 's/spt://g'|sort -n -k1 -r)
    else
        RESULT=$(iptables -nvL $TYPE --line-number 2>/dev/null|grep :|awk -F ':' '{print $2"  " $1}'|awk '{print $2" "$1}'|sort -n -k1 -r)
    fi
    echo "$RESULT" | while read LINE
    do
        LINE_ARRAY=($LINE)
        if [[ ${LINE_ARRAY[1]} && -z $(netstat -tunlp|grep -w ${LINE_ARRAY[1]}) ]];then
            [[ $NETWORK == 1 ]] && ip6tables -D $TYPE ${LINE_ARRAY[0]} || iptables -D $TYPE ${LINE_ARRAY[0]}
        fi
    done
}

clean_iptables INPUT
clean_iptables OUTPUT