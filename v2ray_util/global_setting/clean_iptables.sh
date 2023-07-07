#!/bin/bash
clean_iptables(){
    local type=$1
    if [[ $network == 1 ]];then
        result=$(ip6tables -nvL $type --line-number 2>/dev/null|grep :|awk '{printf "%s %s\n",$1,$NF}'|sed 's/dpt://g'|sed 's/spt://g'|sort -n -k1 -r)
    else
        result=$(iptables -nvL $type --line-number 2>/dev/null|grep :|awk -F ':' '{print $2"  " $1}'|awk '{print $2" "$1}'|sort -n -k1 -r)
    fi
    echo "$result" | while read line
    do
        line_array=($line)
        if [[ ${line_array[1]} && -z $(netstat -tunlp|grep -w ${line_array[1]}) ]];then
            [[ $network == 1 ]] && ip6tables -D $type ${line_array[0]} || iptables -D $type ${line_array[0]}
        fi
    done
}

clean_iptables INPUT
clean_iptables OUTPUT
