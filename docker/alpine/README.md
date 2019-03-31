## How To Use
1. close Firewall
```
systemctl stop firewalld.service
systemctl disable firewalld.service
```
2. run command
```
docker run -d --name v2ray --restart always --network host jrohy/v2ray:alpine
```
3. check v2ray info
```
docker exec v2ray bash -c "v2ray info"
```