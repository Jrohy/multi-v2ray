#!/bin/bash

if [[ ! -e /etc/v2ray ]];then
    mkdir /etc/v2ray
    v2ray new >/dev/null 2>&1
fi

touch /.run.log
/usr/bin/v2ray/v2ray -config=/etc/v2ray/config.json > /.run.log &

tail -f /.run.log