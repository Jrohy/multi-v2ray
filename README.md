
<!-- vim-markdown-toc GFM -->

* [V2ray.fun](#v2rayfun)
    * [功能](#功能)
    * [安装命令](#安装命令)
    * [升级命令](#升级命令)
    * [卸载命令](#卸载命令)
    * [截图](#截图)
    * [系统要求](#系统要求)
    * [软件要求](#软件要求)
    * [更新日志](#更新日志)
    * [特别说明](#特别说明)
    * [感谢](#感谢)

<!-- vim-markdown-toc -->

# V2ray.fun
V2ray控制脚本，向导式更改端口，加密方式，传输协议，享受V2ray的乐趣~  

相对[原版](https://github.com/tracyone/v2ray.fun)增加了:
- 查看配置信息显示vmess字符串
- 首次安装时产生随机端口，默认传输配置改为mkcp+随机三种伪装type之一;  
  安装完成显示配置信息, 都是用于快速部署
- 增加修改alterId入口
- 增加开启动态端口
- 增加v2ray升级菜单

## 功能
- 一键 启动 / 停止 / 重启 V2ray 服务端
- 自动随机生成 UUID
- 自助修改端口
- 快速查看服务器连接信息
- 一键下载客户端配置文件（通过szrz程序，xshell，secureCRT还有[macOS的iterm2](https://github.com/Jrohy/v2ray.fun/wiki/MAC使用RZ、SZ远程上传下载文件都支持)都支持）
- 自由更改**传输配置**：
  - 常规TCP
  - HTTP头部伪装
  - WebSocket流量
  - 常规mKCP流量
  - mKCP 伪装 FaceTime通话流量
  - mKCP 伪装 BT下载流量
  - mKCP 伪装 微信视频通话流量

**WebSocket不包括Nginx分流，请自行安装Nginx来分流。**

## 安装命令

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/Jrohy/v2ray.fun/master/install.sh)"
```

## 升级命令
```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/Jrohy/v2ray.fun/master/upgrade.sh)"
```

## 卸载命令
```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/Jrohy/v2ray.fun/master/uninstall.sh)"
```


## 截图

![1](1.png)

![2](2.png)

## 系统要求

- Debian 7 
- **Debian 8（推荐）**
- Debian 9 
- Ubuntu 14 
- Ubuntu 16 
- CentOS 7

**不支持Centos 6**

## 软件要求

请使用**Xshell**连接服务器，以获得完美的中文支持以及配置文件下载功能。

## 更新日志

**2018.5.3**  
支持开启动态端口

**2018.3.23**  
安装完脚本即显示完整的v2ray配置信息,进一步提高v2ray部署速度

**2018.3.8**   
优化菜单显示  
升级v2ray.fun保留配置文件  
首次安装默认配置改为mkcp+随机三种伪装type之一, 用于快速部署v2ray

**2018.3.6**  
增加配置文件vmess字符串生成显示,增加修改alterId的菜单

**2018.3.5**  
第一次安装产生随机端口

**2017.10.16**  
新增TLS功能，自动获取证书。

**2017.9.4**  
第一版通过测试发布。

## 特别说明

有任何问题或者新功能想法欢迎提交 Issue，我会抽空回答。

本程序遵循 GPL v3协议发布，请Fork保留源项目地址，谢谢！


## 感谢

V2ray : [https://v2ray.com](https://v2ray.com)

v2ray.fun的原作者: [YLWS-4617](https://github.com/YLWS-4617)
