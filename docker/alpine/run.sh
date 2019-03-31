#!/bin/bash

if [[ ! -e /etc/v2ray ]];then
    mkdir -p /etc/v2ray
    mkdir -p /var/log/v2ray/
    v2ray clean >/dev/null 2>&1
    v2ray new >/dev/null 2>&1
fi

/usr/bin/v2ray/v2ray -config=/etc/v2ray/config.json