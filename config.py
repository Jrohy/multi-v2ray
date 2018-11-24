#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import configparser

# CONF_FILE_PATH = '/usr/local/multi-v2ray/multi-v2ray.conf'
CONF_FILE_PATH = 'multi-v2ray.conf'

ENV = 'dev-path'
# ENV = 'prod-path'

class Config:

    def __init__(self):
        #读取配置文件
        self.config = configparser.ConfigParser()
        self.config.read(CONF_FILE_PATH)

    def get_path(self, key):
        return self.config.get(ENV, key)

    def get_data(self, key):
        return self.config.get('data', key)

    def get_web(self, key):
        return self.config.get('web', key)

    def set_data(self, key, value):
        self.config.set('data', key, value)
        self.config.write(open(CONF_FILE_PATH,"w"))