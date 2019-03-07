#!/usr/bin/env python3
# coding: utf-8

import importlib
import os
import pkgutil


def submodules(root_module):

    mod_path = root_module.__file__

    fn = os.path.basename(mod_path)
    pathname = os.path.dirname(mod_path)

    if fn not in ("__init__.py", "__init__.pyc"):
        return None

    rst = {}

    for _, name, _ in pkgutil.iter_modules([pathname]):
        mod = importlib.import_module(root_module.__name__ + "." + name)
        rst[name] = mod

    return rst
