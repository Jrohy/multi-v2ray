#!/bin/bash

clean_iptables(){
    TYPE=$1
    RESULT=$(iptables -nvL $TYPE --line-number|grep :|awk -F ':' '{print $2"  " $1}'|awk '{print $2" "$1}'|sort -n -k1 -r)
    echo "$RESULT" | while read LINE
    do
        LINE_ARRAY=($LINE)
        [[ ${LINE_ARRAY[1]} && -z $(lsof -i:${LINE_ARRAY[1]}) ]] && iptables -D $TYPE ${LINE_ARRAY[0]}
    done
}

clean_iptables INPUT
clean_iptables OUTPUT