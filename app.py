#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from flask import Flask, request, jsonify

from writer import NodeWriter, GroupWriter, ClientWriter, GlobalWriter
from loader import Loader

app = Flask(__name__)

loader = Loader()

class ResponseJson:
    def __init__(self, success=True, msg="ok", data=None):
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

@app.route('/list', methods=['GET'])
def node_list():
    loader.load_profile()
    return json.dumps(loader.profile, default=lambda x: x.__dict__, ensure_ascii=False)

@app.route('/user/<group_tag>', methods = ['POST'])
def add_user(group_tag):
    request_data = request.get_data()
    success, msg, kw = True, "add user success!!!", dict()
    if request_data:
        json_request = json.loads(request.get_data())
        kw['email'] = json_request['email']
    try:
        loader.load_profile()
        group_list = loader.profile.group_list
        group = list(filter(lambda group:group.tag == group_tag, group_list))[0]
        nw = NodeWriter(group.tag, group.index)
        nw.create_new_user(**kw)
    except Exception as e:
        success = False
        msg = str(e)
    return jsonify(ResponseJson(success, msg).__dict__)

@app.route('/user/<int:client_index>', methods = ['DELETE'])
def del_user(client_index):
    success, msg = True, "del user success!!!"
    try:
        loader.load_profile()
        group_list = loader.profile.group_list
        group, client_index = find_client(group_list, client_index)
        nw = NodeWriter()
        nw.del_user(group, client_index)
    except Exception as e:
        success = False
        msg = str(e)
    return jsonify(ResponseJson(success, msg).__dict__)

@app.route('/group/<stream_type>', methods = ['POST'])
def add_group(stream_type):
    kw = dict()
    json_request = json.loads(request.get_data())
    port = int(json_request['port'])
    if "data" in json_request:
        kw = json_request['data']
    success, msg = True, "add group success!!!"
    try:
        from writer import stream_list
        stream_list = stream_list()
        stream = list(filter(lambda stream:stream[0] == stream_type, stream_list))[0][1]
        nw = NodeWriter()
        nw.create_new_port(port, stream, **kw)
    except Exception as e:
        success = False
        msg = str(e)
    return jsonify(ResponseJson(success, msg).__dict__)

@app.route('/group/<group_tag>', methods = ['DELETE'])
def del_group(group_tag):
    success, msg = True, "del group success!!!"
    try:
        loader.load_profile()
        group_list = loader.profile.group_list
        group = list(filter(lambda group:group.tag == group_tag, group_list))[0]
        nw = NodeWriter()
        nw.del_port(group)
    except Exception as e:
        success = False
        msg = str(e)
    return jsonify(ResponseJson(success, msg).__dict__)

@app.route('/group/<group_tag>', methods = ['PUT'])
def modify_group(group_tag):
    success, msg = True, "modify group success!!!"
    try:
        json_request = json.loads(request.get_data())
        loader.load_profile()
        group_list = loader.profile.group_list
        group = list(filter(lambda group:group.tag == group_tag, group_list))[0]
        gw = GroupWriter(group.tag, group.index)
        if 'port' in json_request and json_request['port'] != None:
            gw.write_port(json_request['port'])

        if 'ss_password' in json_request and json_request['ss_password'] != None:
            gw.write_ss_password(json_request['ss_password'])

        if 'ss_method' in json_request and json_request['ss_method'] != None:
            gw.write_ss_password(json_request['ss_method'])

        if 'ss_email' in json_request and json_request['ss_email'] != None:
            gw.write_ss_email(json_request['ss_email'])

        if 'tfo' in json_request and json_request['tfo'] != None:
            gw.write_tfo(json_request['tfo'])

        if 'dyp' in json_request and json_request['tfo'] != None:
            dyp_json = json_request['dyp']
            if 'status' in dyp_json and 'aid' in dyp_json:
                gw.write_dyp(bool(dyp_json['status']), int(dyp_json['aid']))

        # if modify_type == 'tls' and json_request['tls'] != None:
        #     gw.write_tls(bool(json_request['status']), crt_file=json_request['crt_file'], key_file=json_request['key_file'], domain=json_request['domain'])
    except Exception as e:
        success = False
        msg = str(e)
    return jsonify(ResponseJson(success, msg).__dict__)

@app.route('/user/<int:client_index>', methods = ['PUT'])
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
    except Exception as e:
        success = False
        msg = str(e)
    return jsonify(ResponseJson(success, msg.format(modify_type)).__dict__)

@app.route('/global', methods = ['PUT'])
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
    except Exception as e:
        success = False
        msg = str(e)
    return jsonify(ResponseJson(success, msg.format(modify_type)).__dict__)

if __name__ == '__main__':
    app.run(debug=True)