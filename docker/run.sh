#!/bin/bash

if [[ ! -e /etc/v2ray ]];then
    mkdir /etc/v2ray
    v2ray new >/dev/null 2>&1
fi

/usr/bin/v2ray/v2ray -config=/etc/v2ray/config.json