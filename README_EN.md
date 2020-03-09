# multi-v2ray
a tool to manage v2ray config with multi-user support  
![](https://img.shields.io/pypi/v/v2ray-util.svg) 
![](https://img.shields.io/docker/pulls/jrohy/v2ray.svg)
![](https://img.shields.io/github/stars/Jrohy/multi-v2ray.svg) 
![](https://img.shields.io/github/forks/Jrohy/multi-v2ray.svg) 
![](https://img.shields.io/github/license/Jrohy/multi-v2ray.svg)

## [中文](README.md)  [English](README_EN.md)

## Features
- V2ray && iptables traffic statistics
- Command line configuration (users and v2ray config)
- Full multi-user support (same port separate UUID & multiple ports)
- Cloudflare CDN mode support
- ipv6 only server (VPS) support
- Docker support
- V2ray Dynamic port suport
- Ban bittorrent
- Range port support
- TcpFastOpen support
- Vmess/Socks5/MTproto share link
- Supported protocols:
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
curl -o v2ray.sh -L https://git.io/JeDsl && bash v2ray.sh
```

update multi-v2ray to latest version
```
curl -o v2ray.sh -L https://git.io/JeDsl && bash v2ray.sh -k
```

uninstall
```
curl -o v2ray.sh -L https://git.io/JeDsl && bash v2ray.sh --remove
```

## Command Line
```bash
v2ray [-h|--help] [options]
    -h, --help           show help message
    -v, --version        show multi-v2ray version
    start                start V2Ray
    stop                 stop V2Ray
    restart              restart V2Ray
    status               check V2Ray status
    new                  create new json profile
    update               update v2ray to latest version
    update.sh            update multi-v2ray to latest version
    add                  random create mkcp + (srtp|wechat-video|utp|dtls|wireguard) fake header group
    add [wechat|utp|srtp|dtls|wireguard|socks|mtproto|ss]     create special protocol, random new port
    del                  delete port group
    info                 check v2ray profile
    port                 modify port
    tls                  modify tls
    tfo                  modify tcpFastOpen
    stream               modify protocol
    cdn                  cdn mode
    stats                v2ray traffic statistics
    iptables             iptables traffic statistics
    clean                clean v2ray log
    log                  check v2ray log
```

## Docker Run
default config will create random port + random header(srtp | wechat-video | utp | dtls) kcp profile  
```
docker run -d --name v2ray --privileged --restart always --network host jrohy/v2ray
```

custom v2ray config.json:
```
docker run -d --name v2ray --privileged -v /path/config.json:/etc/v2ray/config.json --restart always --network host jrohy/v2ray
```

check v2ray profile:
```
docker exec v2ray bash -c "v2ray info"
```

**warning**: if u run with centos, u should close firewall first
```
systemctl stop firewalld.service
systemctl disable firewalld.service
```

## Dependencies
docker: https://hub.docker.com/r/jrohy/v2ray  
pip: https://pypi.org/project/v2ray-util/  
python3: https://github.com/Jrohy/python3-install  
acme: https://github.com/Neilpang/acme.sh
