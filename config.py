#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import configparser

ENV = 'dev'
# ENV = 'prod'

DEV_FILE_PATH = 'multi-v2ray.conf'
PROD_FILE_PATH = '/usr/local/multi-v2ray/multi-v2ray.conf'

class Config:

    def __init__(self):
        #读取配置文件
        self.config_path = eval('{}_FILE_PATH'.format(ENV.upper()))
        self.config = configparser.ConfigParser()
        self.config.read(self.config_path)

    def get_path(self, key):
        return self.config.get('{}-path'.format(ENV), key)

    def get_web(self, key):
        return self.config.get('web', key)

    def get_data(self, key):
        return self.config.get('data', key)

    def set_data(self, key, value):
        self.config.set('data', key, value)
        self.config.write(open(self.config_path, "w"))