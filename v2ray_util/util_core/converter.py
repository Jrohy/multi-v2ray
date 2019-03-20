#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

config_path = "/etc/v2ray/config.json"

class ConfigConverter:
    def __init__(self):
        self.config = self.load()
    
    def load(self):
        '''
        load v2ray profile
        '''
        with open(config_path, 'r') as json_file:
            config = json.load(json_file)
        return config

    def save(self):
        '''
        save v2ray config.json
        '''
        json_dump=json.dumps(self.config, indent=2)
        with open(config_path, 'w') as writer:
            writer.writelines(json_dump)

    def transform(self):
        inbound_list, outbound_list = [], []
        if "inbound" in self.config:
            inbound_list.append(self.config["inbound"])
            del self.config["inbound"]
        if "inboundDetour" in self.config and self.config["inboundDetour"]:
            inbound_list.extend([ x for x in self.config["inboundDetour"] ])
            del self.config["inboundDetour"]
        if inbound_list:
            self.config["inbounds"] = inbound_list

        if "outbound" in self.config:
            outbound_list.append(self.config["outbound"])
            del self.config["outbound"]
        if "outboundDetour" in self.config and self.config["outboundDetour"]:
            outbound_list.extend([ x for x in self.config["outboundDetour"] ])
            del self.config["outboundDetour"]
        if outbound_list:
            self.config["outbounds"] = outbound_list

        # 转换路由
        if "routing" in self.config and "settings" in self.config["routing"]:
            self.config["routing"]["rules"] = self.config["routing"]["settings"]["rules"]
            del self.config["routing"]["strategy"]
            del self.config["routing"]["settings"]
            
        self.save()

print(_("tranfrom to v2ray new version json.."))
ConfigConverter().transform()