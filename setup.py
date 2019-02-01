#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

"""
打包的用的setup必须引入，
"""

VERSION = '3.0'

setup(
    name='v2ray-util',
    version=VERSION,
    package_data={'danmufm': ['template/*', ]},
    description="a tool to manage v2ray config json",
    long_description='just enjoy',
    classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='python v2ray multi-v2ray vmess socks5',
    author='Jrohy',
    author_email='euvkzx@gmail.com',
    url='https://github.com/Jrohy/multi-v2ray',
    license='GPL',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'click',
        'pyOpenSSL'
    ],
    entry_points={
        'console_scripts': [
            'v2ray = v2ray_util.main:menu'
        ]
    },
)