# multi-v2ray
a tool to manage v2ray config json, support multiple user && group manage  
![](https://img.shields.io/pypi/v/v2ray-util.svg) 
![](https://img.shields.io/docker/pulls/jrohy/v2ray.svg)
![](https://img.shields.io/github/stars/Jrohy/multi-v2ray.svg) 
![](https://img.shields.io/github/forks/Jrohy/multi-v2ray.svg) 
![](https://img.shields.io/github/license/Jrohy/multi-v2ray.svg)

## Feature
- V2ray && Iptables Traffic Statistics
- Command line to manage
- Multiple user && port manage
- Dynamic port
- Ban bittorrent
- Range port
- TcpFastOpen
- Vmess/Socks5/MTproto share link
- Support protocol modify:
  - TCP
  - Fake http
  - WebSocket
  - mkcp
  - mKCP + srtp
  - mKCP + utp
  - mKCP + wechat-video
  - mKCP + dtls
  - mKCP + wireguard
  - HTTP/2
  - Socks5
  - MTProto
  - Shadowsocks
  - Quic

## How To Use
new install
```
source <(curl -sL https://git.io/fNgqx)
```

中文版安装
```
source <(curl -sL https://git.io/fNgqx) --zh
```

keep profile to update(保留配置文件更新)
```
source <(curl -sL https://git.io/fNgqx) -k
```

uninstall
```
source <(curl -sL https://git.io/fNgqx) --remove
```

## Command Line
```bash
v2ray [-h|--help] [options]
    -h, --help           get help
    -v, --version        get version
    start                start V2Ray
    stop                 stop V2Ray
    restart              restart V2Ray
    status               check V2Ray status
    new                  create new json profile
    update               update v2ray to latest
    add                  random create mkcp + (srtp | wechat-video | utp | dtls) fake header group
    add [wechat|utp|srtp|dtls|wireguard|socks|mtproto|ss]     create special protocol, random new port
    del                  delete port group
    info                 check v2ray profile
    port                 modify port
    tls                  modify tls
    tfo                  modify tcpFastOpen
    stream               modify protocol
    stats                iptables traffic statistics
    clean                clean v2ray log
    log                  check v2ray log
```

## Docker Run
```
docker run -d --name v2ray --restart always --network host jrohy/v2ray
```
it will create random port + random header(srtp | wechat-video | utp | dtls) kcp profile  

check v2ray profile:
```
docker exec v2ray bash -c "v2ray info"
```

only restart container to make effect when u change v2ray config.json:
```
docker restart v2ray
```

**warning**: if u run with centos, u should close firewall first
```
systemctl stop firewalld.service
systemctl disable firewalld.service
```

## Changelog
see [Changelog](https://github.com/Jrohy/multi-v2ray/blob/master/Changelog.md)

## Dependent
docker: https://hub.docker.com/r/jrohy/v2ray  
pip: https://pypi.org/project/v2ray-util/  
python3: https://github.com/Jrohy/python3-install