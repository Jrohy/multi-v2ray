#!/bin/bash
PORT=$1

[[ $# == 0 ]]  && exit 1 

INPUT_TRAFFIC=$(iptables -nvL INPUT -x|grep $PORT|awk '{sum += $2};END {printf("%.0f\n",sum)}')

OUTPUT_TRAFFIC=$(iptables -nvL OUTPUT -x|grep $PORT|awk '{sum += $2};END {printf("%.0f\n",sum)}')

if [[ $INPUT_TRAFFIC && $OUTPUT_TRAFFIC ]]; then
    TOTAL_TRAFFIC=`expr $INPUT_TRAFFIC + $OUTPUT_TRAFFIC`
    echo "$INPUT_TRAFFIC $OUTPUT_TRAFFIC $TOTAL_TRAFFIC"
fi