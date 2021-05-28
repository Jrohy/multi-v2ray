#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import base64
from urllib.parse import quote
from .utils import ColorStr

__author__ = 'Jrohy'

class Dyport:
    def __init__(self, status=False, aid=0):
        self.status = status
        self.aid = aid

    def __str__(self):
        return "{}, alterId:{}".format(_("open"), self.aid) if self.status else _("close")

class Quic:
    def __init__(self, security="none", key="", header="none"):
        self.security = security
        self.key = key
        self.header = header
    
    def __str__(self):
        return "Security: {0}\nKey: {1}\nHeader: {2}".format(self.security, self.key, self.header)

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
        return ColorStr.green("ss://{}".format(bytes.decode(base64.b64encode(bytes(ss_origin_url, 'utf-8')))))

    def stream(self):
        return "shadowsocks"

class Trojan(User):
    def __init__(self, user_number, password, email):
        super(Trojan, self).__init__(user_number, password, email)
    
    def __str__(self):
        if self.user_info:
            return "Email: {self.user_info}\nPassword: {password}\n".format(self=self, password=self.password)
        else:
            return "Password: {password}\n".format(password=self.password)

    def link(self, ip, port, tls):
        return ColorStr.green("trojan://{0}@{1}:{2}".format(self.password, ip, port))

    def stream(self):
        return "trojan"

class Mtproto(User):
    def __str__(self):
        if self.user_info:
            return "Email: {}\nSecret: {}\n".format(self.user_info, self.password)
        else:
            return "Secret: {}\n".format(self.password)
    
    def link(self, ip, port, tls):
        return ColorStr.green("tg://proxy?server={0}&port={1}&secret={2}".format(ip, port, self.password))

    def stream(self):
        return "mtproto"

class Socks(User):
    def __str__(self):
        return "User: {0}\nPass: {1}\nUDP: true\n".format(self.user_info, self.password)

    def link(self, ip, port, tls):
        if tls == "tls":
            return ColorStr.red(_("HTTPS Socks5 don't support telegram share link"))
        else:
            return ColorStr.green("tg://socks?server={0}&port={1}&user={2}&pass={3}".format(ip, port, self.user_info, self.password))

    def stream(self):
        return "socks"

class Vless(User):
    def __init__(self, uuid, user_number, encryption=None, email=None, network=None, path=None, host=None, header=None, flow="", serviceName="", mode=""):
        super(Vless, self).__init__(user_number, uuid, email)
        self.encryption = encryption
        self.path = path
        self.host = host
        self.header = header
        self.network = network
        self.flow = flow
        self.serviceName = serviceName
        self.mode = mode

    def __str__(self):
        email = ""
        if self.user_info:
            email = "Email: {}".format(self.user_info)
        result = '''
{email}
ID: {password}
Encryption: {self.encryption}
Network: {network}
'''.format(self=self, password=self.password, email=email, network=self.stream()).strip() + "\n"
        return result
    
    def stream(self):
        if self.network == "ws":
            return "WebSocket host: {0}, path: {1}".format(self.host, self.path)
        elif self.network == "tcp":
            return "tcp"
        elif self.network == "grpc":
            return "grpc serviceName: {}, mode: {}".format(self.serviceName, self.mode)
        elif self.network == "kcp":
            result = "kcp"
            if self.header and self.header != 'none':
                result = "{} {}".format(result, self.header)
            if self.path != "":
                result = "{} seed: {}".format(result, self.path)
            return result

    def link(self, ip, port, tls):
        result_link = "vless://{s.password}@{ip}:{port}?encryption={s.encryption}".format(s=self, ip=ip, port=port)
        if tls == "tls":
            result_link += "&security=tls"
        elif tls == "xtls":
            result_link += "&security=xtls&flow={}".format(self.flow)
        if self.network == "ws":
            result_link += "&type=ws&host={0}&path={1}".format(self.host, quote(self.path))
        elif self.network == "tcp":
            result_link += "&type=tcp"
        elif self.network == "grpc":
            result_link += "&type=grpc&serviceName={}&mode={}".format(self.serviceName, self.mode)
        elif self.network == "kcp":
            result_link += "&type=kcp&headerType={0}&seed={1}".format(self.header, self.path)
        return ColorStr.green(result_link)

class Vmess(User):
    def __init__(self, uuid, alter_id: int, network: str, user_number, *, path=None, host=None, header=None, email=None, quic=None):
        super(Vmess, self).__init__(user_number, uuid, email)
        self.alter_id = alter_id
        self.network = network
        self.path = path
        self.host = host
        self.header = header
        self.quic = quic
        if quic:
            self.header = quic.header
            self.host = quic.security
            self.path = quic.key

    def stream(self):
        network = ""
        if self.network == "quic":
            network = "Quic\n{}".format(self.quic)
        elif self.network == "h2":
            network = "HTTP/2 path: {}".format(self.path)
        elif self.network == "ws":
            network = "WebSocket host: {0}, path: {1}".format(self.host, self.path)
        elif self.network == "tcp":
            if self.host:
                network = "tcp host: {0}".format(self.host)
            else:
                network = "tcp"
        elif self.network == "kcp":
            network = "kcp"
            if self.header and self.header != 'none':
                network = "{} {}".format(network, self.header)
            if self.path != "":
                network = "{} seed: {}".format(network, self.path)
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
        result_link = "vmess://{}".format(bytes.decode(base64.b64encode(bytes(json_data, 'utf-8'))))
        return ColorStr.green(result_link)

class Group:
    def __init__(self, ip, port, *, end_port=None, tfo=None, tls="none", dyp=Dyport(), index=0, tag='A'):
        self.ip = ip
        self.port = port
        self.end_port = end_port
        self.tag = tag
        self.node_list = []
        self.tfo = tfo
        self.tls = tls
        self.dyp = dyp
        self.protocol = None
        self.index = index

    def show_node(self, index):
        tfo = "TcpFastOpen: {}".format(self.tfo) if self.tfo != None else ""
        dyp = "DynamicPort: {}".format(self.dyp) if self.dyp.status else ""
        port_way = "-{}".format(self.end_port) if self.end_port else ""
        node = self.node_list[index]
        if self.tls == "tls":
            tls = _("open")
        elif self.tls == "xtls":
            tls = "xtls {0}, flow: {1}".format(_("open"), node.flow)
        else:
            tls = _("close")
        result = '''
{node.user_number}.
Group: {self.tag}
IP: {color_ip}
Port: {self.port}{port_way}
TLS: {tls}
{node}{tfo}
{dyp}'''.format(self=self, color_ip=ColorStr.fuchsia(self.ip), port_way=port_way, node=node,tfo=tfo, dyp=dyp,tls=tls)
        link = node.link(self.ip, int(self.port), self.tls)
        if link:
            result += "{}\n\n".format(link)
        return result

    # print一个实例打印的字符串
    def __str__(self):
        tfo = "TcpFastOpen: {}".format(self.tfo) if self.tfo != None else ""
        dyp = "DynamicPort: {}".format(self.dyp) if self.dyp.status else ""
        port_way = "-{}".format(self.end_port) if self.end_port else ""
        if self.tls == "tls":
            tls = _("open")
        elif self.tls == "xtls":
            tls = "xtls {0}, flow: {1}".format(_("open"), self.node_list[0].flow)
        else:
            tls = _("close")
        result = ""
        for node in self.node_list:
            temp = '''
{node.user_number}.
Group: {self.tag}
IP: {color_ip}
Port: {self.port}{port_way}
TLS: {tls}
{node}{tfo}
{dyp}
            '''.format(self=self, color_ip=ColorStr.fuchsia(self.ip), node=node,tfo=tfo,dyp=dyp,tls=tls, port_way=port_way)
            link = node.link(self.ip, int(self.port), self.tls)
            result = "{0}{1}\n\n".format(result, temp.strip())
            if link:
                result += "{}\n\n".format(link)             
        return result

    # 直接调用实例和打印一个实例显示的字符串一样
    def __repr__ (self):
        return self.__str__