#!/bin/bash
export PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

#重装V2ray.fun
rm -rf /usr/local/v2ray.fun
cd /usr/local/
git clone https://github.com/FunctionClub/v2ray.fun
cd /usr/local/v2ray.fun/
chmod +x *.py

#重装操作菜单
rm -rf /usr/local/bin/v2ray
cp /usr/local/v2ray.fun/v2ray /usr/local/bin/
chmod +x /usr/local/bin/v2ray

#更新Vray主程序
bash <(curl -L -s https://install.direct/go.sh)

#初始化环境
rm -rf /etc/v2ray/config.json
mv /usr/local/v2ray.fun/json_template/server.json /etc/v2ray/config.json
UUID=$(cat /proc/sys/kernel/random/uuid)
sed -i "s/cc4f8d5b-967b-4557-a4b6-bde92965bc27/${UUID}/g" /etc/v2ray/config.json
python /usr/local/v2ray.fun/genclient.py
python /usr/local/v2ray.fun/openport.py

clear
echo "脚本已更新！"
