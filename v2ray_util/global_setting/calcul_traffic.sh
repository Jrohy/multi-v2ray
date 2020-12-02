#!/bin/bash
PORT=$1

NETWORK=$2

[[ $# == 0 ]]  && exit 1 

if [[ $NETWORK ]];then
    INPUT_TRAFFIC=$(ip6tables -nvL INPUT -x 2>/dev/null|grep $PORT|awk '{sum += $2};END {printf("%.0f\n",sum)}')

    OUTPUT_TRAFFIC=$(ip6tables -nvL OUTPUT -x 2>/dev/null|grep $PORT|awk '{sum += $2};END {printf("%.0f\n",sum)}') 
else
    INPUT_TRAFFIC=$(iptables -nvL INPUT -x 2>/dev/null|grep $PORT|awk '{sum += $2};END {printf("%.0f\n",sum)}')

    OUTPUT_TRAFFIC=$(iptables -nvL OUTPUT -x 2>/dev/null|grep $PORT|awk '{sum += $2};END {printf("%.0f\n",sum)}')
fi

if [[ $INPUT_TRAFFIC && $OUTPUT_TRAFFIC ]]; then
    TOTAL_TRAFFIC=`expr $INPUT_TRAFFIC + $OUTPUT_TRAFFIC`
    echo "$INPUT_TRAFFIC $OUTPUT_TRAFFIC $TOTAL_TRAFFIC"
fi