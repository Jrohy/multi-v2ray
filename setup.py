#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

import v2ray_util

setup(
    name='v2ray_util',
    version=v2ray_util.__version__,
    description="a tool to manage v2ray config json",
    long_description=open('README.rst').read(),
    keywords='python v2ray multi-v2ray vmess socks5',
    author='Jrohy',
    author_email='euvkzx@gmail.com',
    url='https://github.com/Jrohy/multi-v2ray',
    license='GPL',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3',
    install_requires=[
        'pyOpenSSL'
    ],
    entry_points={
        'console_scripts': [
            'v2ray_util = v2ray_util.main:menu'
        ]
    },
    classifiers=[
        'Topic :: Utilities',
        'Development Status :: 5 - Production/Stable',
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)