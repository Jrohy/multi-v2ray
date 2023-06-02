#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

import v2ray_util

with open("README.md", "r", encoding='UTF-8') as fh:
    long_description = fh.read()

setup(
    name='v2ray-util',
    version=v2ray_util.__version__,
    description="a tool to manage v2ray config json",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='python v2ray multi-v2ray vmess socks5 vless trojan xray xtls reality',
    author='Jrohy',
    author_email='euvkzx@gmail.com',
    url='https://github.com/Jrohy/multi-v2ray',
    license='GPL',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3',
    entry_points={
        'console_scripts': [
            'v2ray-util = v2ray_util.main:menu'
        ]
    },
    classifiers=[
        'Topic :: Utilities',
        'Development Status :: 5 - Production/Stable',
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ]
)