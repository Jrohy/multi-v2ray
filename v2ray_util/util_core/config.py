#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pkg_resources
import configparser
from v2ray_util import run_type

CONF_FILE = '/etc/v2ray_util/util.cfg'
DATA_FILE = 'util.dat' if run_type == "v2ray" else 'xray.dat'

class Config:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config_path = CONF_FILE
        self.data_path = pkg_resources.resource_filename('v2ray_util', DATA_FILE)
        self.json_path = pkg_resources.resource_filename('v2ray_util', "json_template")
        self.config.read(self.config_path)

    def get_path(self, key):
        if key == 'config_path' and run_type == 'xray':
            return '/etc/xray/config.json'
        return self.config.get('path', key)

    def get_data(self, key):
        return self.config.get('data', key)

    def set_data(self, key, value):
        self.config.set('data', key, value)
        self.config.write(open(self.config_path, "w"))