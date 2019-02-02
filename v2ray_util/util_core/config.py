#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pkg_resources
import configparser

ENV = 'prod'
CONF_FILE = 'util.cfg'

class Config:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config_path = pkg_resources.resource_filename(__name__, CONF_FILE)
        self.json_path = pkg_resources.resource_listdir('v2ray_util', "json_template")
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