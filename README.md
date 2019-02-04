# v2ray-util
a tool to manage v2ray config json, support multiple user && group manage  
![](https://img.shields.io/pypi/v/v2ray-util.svg) 
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
- Support protocol modify：
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

## Install
```
pip install v2ray-util
```
run `v2ray-util` to start manage v2ray  
this tool only support **python3+**


## Command Line
```bash
v2ray-util [-h|--help] [options]
    -h, --help           get help
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
```