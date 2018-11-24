#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
from flask import request, jsonify, Blueprint

from writer import NodeWriter, GroupWriter, ClientWriter, GlobalWriter
from loader import Loader

func_router = Blueprint('func_router', __name__)

loader = Loader()

class ResponseJson:
    def __init__(self, success=True, msg="success", data=None):
        self.success = success
        self.msg = msg
        self.data = data

def find_client(group_list, client_index):
    find, group = False, None
    for single_group in group_list:
        if find:
            break
        for index, node in enumerate(single_group.node_list):
            if node.user_number == client_index:
                client_index = index
                group = single_group
                find = True
                break
    return group, client_index

@func_router.route('/list', methods=['GET'])
def node_list():
    loader.load_profile()
    return json.dumps(loader.profile, default=lambda x: x.__dict__, ensure_ascii=False)

@func_router.route('/manage/<action>', methods=['POST'])
def manage(action):
    success, msg, result = True, "{} v2ray success!!!", None
    try:
        if action in ['start', 'stop', 'restart']:
            os.system("service v2ray {}".format(action))
        else:
            raise ValueError("{} action not found".format(action))
    except Exception as e:
        success = False
        msg = str(e)
    return jsonify(ResponseJson(success, msg, result).__dict__)

@func_router.route('/user', methods = ['POST'])
def add_user():
    success, msg, kw = True, "add user success!!!", dict()
    try:
        json_request = json.loads(request.get_data())
        group_tag = json_request['group_tag']
        kw['email'] = json_request['email']
        loader.load_profile()
        group_list = loader.profile.group_list
        group = list(filter(lambda group:group.tag == group_tag, group_list))[0]
        nw = NodeWriter(group.tag, group.index)
        nw.create_new_user(**kw)
    except Exception as e:
        success = False
        msg = str(e)
    return jsonify(ResponseJson(success, msg).__dict__)

@func_router.route('/user/<int:client_index>', methods = ['DELETE'])
def del_user(client_index):
    success, msg = True, "del user {} success!!!"
    try:
        loader.load_profile()
        group_list = loader.profile.group_list
        group, client_index = find_client(group_list, client_index)
        nw = NodeWriter()
        nw.del_user(group, client_index)
    except Exception as e:
        success = False
        msg = str(e)
    return jsonify(ResponseJson(success, msg.format(client_index)).__dict__)

@func_router.route('/group', methods = ['POST'])
def add_group():
    success, msg, kw, stream_type = True, "add group {} success!!!", dict(), ""
    try:
        json_request = json.loads(request.get_data())
        port = int(json_request['port'])
        stream_type = json_request['stream_type']
        if stream_type not in ['wireguard', 'dtls', 'wechat', 'utp', 'srtp', 'mtproto', 'socks', 'ss']:
            raise ValueError("stream_type {} not found".format(stream_type))
        if "data" in json_request:
            kw = json_request['data']
        from writer import stream_list
        stream_list = stream_list()
        stream = list(filter(lambda stream:stream[0] == stream_type, stream_list))[0][1]
        nw = NodeWriter()
        nw.create_new_port(port, stream, **kw)
    except Exception as e:
        success = False
        msg = str(e)
    return jsonify(ResponseJson(success, msg.format(stream_type)).__dict__)

@func_router.route('/group/<group_tag>', methods = ['DELETE'])
def del_group(group_tag):
    success, msg = True, "del group {} success!!!"
    try:
        loader.load_profile()
        group_list = loader.profile.group_list
        group = list(filter(lambda group:group.tag == group_tag, group_list))[0]
        nw = NodeWriter()
        nw.del_port(group)
    except Exception as e:
        success = False
        msg = str(e)
    return jsonify(ResponseJson(success, msg.format(group_tag)).__dict__)

@func_router.route('/group/<group_tag>', methods = ['PUT'])
def modify_group(group_tag):
    success, msg = True, "modify group {} success!!!"
    try:
        json_request = json.loads(request.get_data())
        modify_type = json_request['modify_type']
        value = json_request['value']
        loader.load_profile()
        group_list = loader.profile.group_list
        group = list(filter(lambda group:group.tag == group_tag, group_list))[0]
        gw = GroupWriter(group.tag, group.index)
        method = 'write_' + modify_type
        if hasattr(gw, method):
            func = getattr(gw, method)
            if modify_type == "dyp":
                func(bool(value['status']), int(value['aid']))
            else:
                func(value)
        else:
            raise RuntimeError("{} method not found".format(method))
    except Exception as e:
        success = False
        msg = str(e)
    return jsonify(ResponseJson(success, msg.format(modify_type)).__dict__)

@func_router.route('/user/<int:client_index>', methods = ['PUT'])
def modify_user(client_index):
    success, msg, modify_type = True, "modify user {} success!!!", ""
    try:
        json_request = json.loads(request.get_data())
        modify_type = json_request['modify_type']
        value = json_request['value']
        loader.load_profile()
        group_list = loader.profile.group_list
        group, client_index = find_client(group_list, client_index)
        cw = ClientWriter(group.tag, group.index, client_index)
        method = 'write_' + modify_type
        if hasattr(cw, method):
            func = getattr(cw, method)
            func(value)
        else:
            raise RuntimeError("{} method not found".format(method))
    except Exception as e:
        success = False
        msg = str(e)
    return jsonify(ResponseJson(success, msg.format(modify_type)).__dict__)

@func_router.route('/global', methods = ['PUT'])
def modify_global():
    success, msg, modify_type = True, "modify global {} success!!!", ""
    try:
        json_request = json.loads(request.get_data())
        modify_type = json_request['modify_type']
        value = json_request['value']
        loader.load_profile()
        group_list = loader.profile.group_list
        gw = GlobalWriter(group_list)
        method = 'write_' + modify_type
        if hasattr(gw, method):
            func = getattr(gw, method)
            func(value)
        else:
            raise RuntimeError("{} method not found".format(method))
    except Exception as e:
        success = False
        msg = str(e)
    return jsonify(ResponseJson(success, msg.format(modify_type)).__dict__)