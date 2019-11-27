#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import pickle

from .config import Config
from .profile import Profile

class Loader:
    def __init__(self):
        config = Config()
        self.config_path = config.get_path("config_path")
        self.path = config.data_path
        self.profile = None
        self.load_profile()

    def load_profile(self):
        try:
            if os.path.exists(self.path):
                with open(self.path, 'rb') as reader:
                    self.profile = pickle.load(reader)
                if os.path.getmtime(self.profile.path) != self.profile.modify_time:
                    raise ValueError
                if not hasattr(self.profile, "network"):
                    raise ValueError
            else:
                raise FileNotFoundError
        except Exception:
            self.profile = Profile()
            self.save_profile()

    def save_profile(self):
        with open(self.path, 'wb') as writer:
            pickle.dump(self.profile, writer)