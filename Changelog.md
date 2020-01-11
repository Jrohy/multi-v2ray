# Change Log
## [v3.7.7](https://github.com/Jrohy/multi-v2ray/releases/tag/v3.7.7)(2020-01-11)
- fix [#279](https://github.com/Jrohy/multi-v2ray/issues/279): 生成随机端口时进行端口检测是否占用, 同时不再用lsof来检测端口占用(去掉依赖), 换成python原生socket来检测

## [v3.7.6](https://github.com/Jrohy/multi-v2ray/releases/tag/v3.7.6)(2020-01-03)
- 添加 docker 容器内update.sh命令支持

## [v3.7.5](https://github.com/Jrohy/multi-v2ray/releases/tag/v3.7.5)(2019-11-29)
- 加入生成随机邮箱 [#253](https://github.com/Jrohy/multi-v2ray/issues/253)
- fix [#255](https://github.com/Jrohy/multi-v2ray/issues/255): 纯IPV6的vps获取SSL证书失败,acme.sh无法安装
- fix [#256](https://github.com/Jrohy/multi-v2ray/issues/256)

## [v3.7.4](https://github.com/Jrohy/multi-v2ray/releases/tag/v3.7.4)(2019-11-28)
- 测试支持纯ipv6 vps, 安装脚本路径更换

## [v3.7.3](https://github.com/Jrohy/multi-v2ray/releases/tag/v3.7.3)(2019-11-17)
- 添加完整的docker功能, 包括实现容器内iptables流量统计、证书申请、命令补全  
  实现iptables流量统计起容器时必须加入--privileged

## [v3.7.2](https://github.com/Jrohy/multi-v2ray/releases/tag/v3.7.2)(2019-11-15)
- 优化脚本输入体验, 单个字符输入免回车

## [v3.7.1](https://github.com/Jrohy/multi-v2ray/releases/tag/v3.7.1)(2019-11-12)
- fix [#244](https://github.com/Jrohy/multi-v2ray/issues/244), 修复v2ray流量统计bug
- 修改v2ray流量统计命令行为`v2ray stats`, iptables流量统计为`v2ray iptables`

## [v3.7.0](https://github.com/Jrohy/multi-v2ray/releases/tag/v3.7.0)(2019-11-07)
- 添加更多Cloudcflare cdn 端口, 端口详见: [Identifying network ports compatible with Cloudflare's proxy
](https://support.cloudflare.com/hc/en-us/articles/200169156-Identifying-network-ports-compatible-with-Cloudflare-s-proxy)

## [v3.6.8](https://github.com/Jrohy/multi-v2ray/releases/tag/v3.6.8)(2019-11-05)
- 优化v2ray流量统计查看

## [v3.6.7](https://github.com/Jrohy/multi-v2ray/releases/tag/v3.6.7)(2019-10-03)
- 选择组时输入的字母不再区分大小写.

## [v3.6.6](https://github.com/Jrohy/multi-v2ray/releases/tag/v3.6.6)(2019-10-03)
- fixed: [#231](https://github.com/Jrohy/multi-v2ray/issues/231)

## [v3.6.5](https://github.com/Jrohy/multi-v2ray/releases/tag/v3.6.5)(2019-09-28)
- 优化docker平台服务管理

## [v3.6.4](https://github.com/Jrohy/multi-v2ray/releases/tag/v3.6.4)(2019-09-28)
- 添加`v2ray update.sh`命令来更新multi-v2ray脚本

## [v3.6.3](https://github.com/Jrohy/multi-v2ray/releases/tag/v3.6.3)(2019-09-21)
- Added: 80端口cdn关闭(去掉域名)
- Added: 随机生成kcp header时增加wireguard header
- Changed: service命令变为systemctl

## [v3.6.0](https://github.com/Jrohy/multi-v2ray/releases/tag/v3.6.0)(2019-09-21)
- Fixed: #218
- Fixed: v2ray重启失败时提示重启成功
- Fixed: 没有修改配置文件却触发v2ray重启
- Added: cdn 命令行传参(v2ray cdn)

## [v3.5.2](https://github.com/Jrohy/multi-v2ray/releases/tag/v3.5.2)(2019-09-19)
- 支持80端口和443端口的cdn模式
- 支持域名按group存储

## [v3.2.0](https://github.com/Jrohy/multi-v2ray/releases/tag/v3.2.0)(2019-04-12)
- 修复单独pip安装时因为翻译'_'模块无法使用的问题
- 支持v2rayN quic vmess分享格式

## [v3.1.0](https://github.com/Jrohy/multi-v2ray/releases/tag/v3.1.0)(2019-03-22)
- 修复翻译错误, 流量统计乱码

## [v3.0.7](https://github.com/Jrohy/multi-v2ray/releases/tag/v3.0.7)(2019-03-22)
- support chinese && english switch
- check v2ray log
- [#163](https://github.com/Jrohy/multi-v2ray/issues/163)
- [#168](https://github.com/Jrohy/multi-v2ray/issues/168)

## [v3.0.6](https://github.com/Jrohy/multi-v2ray/releases/tag/v3.0.6)(2019-03-17)
- Change to pip install
- [#152](https://github.com/Jrohy/multi-v2ray/issues/152)
- [#155](https://github.com/Jrohy/multi-v2ray/issues/155)

## [v2.6.3.1](https://github.com/Jrohy/multi-v2ray/releases/tag/v2.6.3.1)(2019-01-10)
- fix some bug

## [v2.6.3](https://github.com/Jrohy/multi-v2ray/releases/tag/v2.6.3)(2018-12-25)
- [#107](https://github.com/Jrohy/multi-v2ray/issues/107)
- [#108](https://github.com/Jrohy/multi-v2ray/issues/108)
- support zsh

## [v2.6.2](https://github.com/Jrohy/multi-v2ray/releases/tag/v2.6.2)(2018-12-23)
- [#106](https://github.com/Jrohy/multi-v2ray/issues/106)

## [v2.6.1](https://github.com/Jrohy/multi-v2ray/releases/tag/v2.6.1)(2018-12-21)
- [#99](https://github.com/Jrohy/multi-v2ray/issues/99)
- Fix del mtproto port

## [v2.6.0](https://github.com/Jrohy/multi-v2ray/releases/tag/v2.6.0)(2018-12-17)
- [#95](https://github.com/Jrohy/multi-v2ray/issues/95)
- [#96](https://github.com/Jrohy/multi-v2ray/issues/96)
- 增加iptables端口流量统计

## [v2.5.3](https://github.com/Jrohy/multi-v2ray/releases/tag/v2.5.3)(2018-12-08)
- [#82](https://github.com/Jrohy/multi-v2ray/issues/82)
- Fix force update bug

## [v2.5.2](https://github.com/Jrohy/multi-v2ray/releases/tag/v2.5.2)(2018-12-06)
- [#78](https://github.com/Jrohy/multi-v2ray/issues/78)
- [#80](https://github.com/Jrohy/multi-v2ray/issues/80)

## [v2.5.1](https://github.com/Jrohy/multi-v2ray/releases/tag/v2.5.1)(2018-12-03)
- 加入更新脚本特定版本指令

## [v2.5.0](https://github.com/Jrohy/multi-v2ray/releases/tag/v2.5.0)(2018-12-02)
- 更新策略更改, 只用最新的Release版本更新, 亦可指定版本更新(回退)
- 增加版本信息显示

## [v2.4](https://github.com/Jrohy/multi-v2ray/releases/tag/v2.4)(2018-11-29)
- 支持Quic
- 加入更新v2ray到特定版本的指令

## [v2.3](https://github.com/Jrohy/multi-v2ray/releases/tag/v2.3)(2018-11-27)
- Add Flask web接口
- 精简json模板

## [v2.2](https://github.com/Jrohy/multi-v2ray/releases/tag/v2.2)(2018-11-20)
- 加入禁止BT

## [v2.1](https://github.com/Jrohy/multi-v2ray/releases/tag/v2.1)(2018-11-19)
- 代码重构，加入json文件缓存

## [v2.0](https://github.com/Jrohy/multi-v2ray/releases/tag/v2.0)(2018-10-09)
- 代码重构，加入json文件缓存

## [v1.0](https://github.com/Jrohy/multi-v2ray/releases/tag/v1.0)(2018-09-23)