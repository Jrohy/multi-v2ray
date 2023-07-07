#!/bin/bash
port=$1

network=$2

[[ $# == 0 ]]  && exit 1 

if [[ $network ]];then
    input_traffic=$(ip6tables -nvL INPUT -x 2>/dev/null|grep $port|awk '{sum += $2};END {printf("%.0f\n",sum)}')

    output_traffic=$(ip6tables -nvL OUTPUT -x 2>/dev/null|grep $port|awk '{sum += $2};END {printf("%.0f\n",sum)}') 
else
    input_traffic=$(iptables -nvL INPUT -x 2>/dev/null|grep $port|awk '{sum += $2};END {printf("%.0f\n",sum)}')

    output_traffic=$(iptables -nvL OUTPUT -x 2>/dev/null|grep $port|awk '{sum += $2};END {printf("%.0f\n",sum)}')
fi

if [[ $input_traffic && $output_traffic ]]; then
    total_traffic=`expr $input_traffic + $output_traffic`
    echo "$input_traffic $output_traffic $total_traffic"
fi
