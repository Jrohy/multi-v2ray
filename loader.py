#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import pickle

from profile import Profile

class Loader:
    def __init__(self, path='/usr/local/multi-v2ray/multi-v2ray.dat', config_path=None):
        self.config_path = config_path
        self.path = path
        self.profile = None
        self.load_profile()

    def load_profile(self):
        try:
            if os.path.exists(self.path):
                with open(self.path, 'rb') as reader:
                    self.profile = pickle.load(reader)
                if os.path.getmtime(self.profile.path) != self.profile.modify_time:
                    raise ValueError
            else:
                raise FileNotFoundError
        except Exception:
            if self.config_path:
                self.profile = Profile(self.config_path)
            else:
                self.profile = Profile()
            self.save_profile()

    def save_profile(self):
        with open(self.path, 'wb') as writer:
            pickle.dump(self.profile, writer)