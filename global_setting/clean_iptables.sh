#!/bin/bash

RESULT=$(iptables -nvL INPUT --line-number|grep dpt|awk '{print $1"  " $14}'|sed 's/dpt://g'|sort -n -k1 -r)
echo "$RESULT" | while read LINE
do
    LINE_ARRAY=($LINE)
    [[ ${LINE_ARRAY[1]} && -z $(lsof -i:${LINE_ARRAY[1]}) ]] && iptables -D INPUT ${LINE_ARRAY[0]}
done