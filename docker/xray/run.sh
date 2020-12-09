#!/bin/bash

if [[ ! -e /etc/xray ]];then
    mkdir /etc/xray
    xray new >/dev/null 2>&1
fi

touch /.run.log
/usr/bin/xray/xray -config=/etc/xray/config.json > /.run.log &

tail -f /.run.log