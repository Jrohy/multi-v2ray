#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import base64

# from base_util.tool_box import color_str, Color

__author__ = 'Jrohy'

class Dyport:
    def __init__(self, status=False, aid=0):
        self.status = status
        self.aid = aid

    def __str__(self):
        return "开启,alterId为{}".format(self.aid) if self.status else "关闭"

class User:
    def __init__(self, user_number, password, user_info=None):
        """
        user_info可能是email, 也可能user_name, 具体取决于group的protocol
        """
        self.__password = password
        self.user_info = user_info
        self.user_number = user_number

    @property
    def password(self):
        return self.__password

class SS(User):
    def __init__(self, user_number, password, method, user_info):
        super(SS, self).__init__(user_number, password, user_info)
        self.method = method
    
    def __str__(self):
        if self.user_info:
            return "Email: {self.user_info}\nMethod: {self.method}\nPassword: {password}\n".format(self=self, password=self.password)
        else:
            return "Method: {self.method}\nPassword: {password}\n".format(self=self, password=self.password)

    def link(self, ip, port, tls):
        ss_origin_url = "{0}:{1}@{2}:{3}".format(self.method, self.password, ip, port)
        return "ss://{}".format(bytes.decode(base64.b64encode(bytes(ss_origin_url, 'utf-8'))))

    def stream(self):
        return "shadowsocks"

class Mtproto(User):
    def __str__(self):
        if self.user_info:
            return "Email: {}\nSecret: {}\n".format(self.user_info, self.password)
        else:
            return "Secret: {}\n".format(self.password)
    
    def link(self, ip, port, tls):
        return "tg://proxy?server={0}&port={1}&secret={2}".format(ip, port, self.password)

    def stream(self):
        return "mtproto"

class Socks(User):
    def __str__(self):
        return "User: {0}\nPass: {1}\nUDP: true\n".format(self.user_info, self.password)

    def link(self, ip, port, tls):
        if tls == "tls":
            return "HTTPS的Socks5不支持tg的分享连接. 请自行配合设置BifrostV等软件使用"
        else:
            return "tg://socks?server={0}&port={1}&user={2}&pass={3}".format(ip, port, self.user_info, self.password)

    def stream(self):
        return "socks"

class Vmess(User):
    def __init__(self, uuid, alter_id: int, network: str, user_number, *, path=None, host=None, header=None, email=None):
        super(Vmess, self).__init__(user_number, uuid, email)
        self.alter_id = alter_id
        self.network = network
        self.path = path
        self.host = host
        self.header = header

    def stream(self):
        if self.network == "h2":
            network = "HTTP/2 path: {}".format(self.path)
        elif self.network == "ws":
            network = "WebSocket host: {0}, path: {1}".format(self.host, self.path)
        elif self.network == "tcp":
            if self.host:
                network = "tcp host: {0}".format(self.host)
            else:
                network = "tcp"
        else:
            if self.header and self.header != 'none':
                network = "{} {}".format(self.network, self.header)
            else:
                network = "{}".format(self.network)
        return network

    def __str__(self):
        email = ""
        if self.user_info:
            email = "Email: {}".format(self.user_info)
        result = '''
{email}
UUID: {uuid}
Alter ID: {self.alter_id}
Network: {network}
'''.format(self=self, uuid=self.password, email=email, network=self.stream()).strip() + "\n"
        return result

    def link(self, ip, port, tls):
        json_dict = {
            "v": "2",
            "ps": "",
            "add": ip,
            "port": port,
            "aid": self.alter_id,
            "type": self.header,
            "net": self.network,
            "path": self.path,
            "host": self.host,
            "id": self.password,
            "tls": tls
        }
        json_data = json.dumps(json_dict)
        return "vmess://{}".format(bytes.decode(base64.b64encode(bytes(json_data, 'utf-8'))))

class Group:
    def __init__(self, ip, port, *, tls="", tfo=None, dyp=Dyport(), index=-1, tag='A'):
        self.ip = ip
        self.port = port
        self.tag = tag
        self.node_list = []
        self.tfo = tfo
        self.tls = tls
        self.dyp = dyp
        # -1 为A组, 0 ~ .. 为inboundDetour 里面的对应坐标
        self.index = index

    def show_node(self, index):
        tls = "开启"if self.tls else "关闭"
        tfo = "TcpFastOpen: {}".format(self.tfo) if self.tfo != None else ""
        dyp = "DynamicPort: {}".format(self.dyp) if self.dyp.status else ""
        node = self.node_list[index]
        result = '''
{node.user_number}
Group: {self.tag}
IP: {self.ip}
Port: {self.port}
TLS: {tls}
{node}{tfo}{dyp}
{link}
            '''.format(self=self,node=node,tfo=tfo,dyp=dyp,tls=tls, link=node.link(self.ip, self.port, self.tls))
        return result

    # print一个实例打印的字符串
    def __str__(self):
        tls = "开启"if self.tls else "关闭"
        tfo = "TcpFastOpen: {}".format(self.tfo) if self.tfo != None else ""
        dyp = "DynamicPort: {}".format(self.dyp) if self.dyp.status else ""
        result = ""
        for node in self.node_list:
            temp = '''
{node.user_number}
Group: {self.tag}
IP: {self.ip}
Port: {self.port}
TLS: {tls}
{node}{tfo}{dyp}
            '''.format(self=self, node=node,tfo=tfo,dyp=dyp,tls=tls)
            result = "{0}{1}\n\n{2}\n\n".format(result, temp.strip(), node.link(self.ip, self.port, self.tls))
        return result

    # 直接调用实例和打印一个实例显示的字符串一样
    def __repr__ (self):
        return self.__str__