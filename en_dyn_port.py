#! /usr/bin/env python
# -*- coding: utf-8 -*-
import readjson
import writejson
from v2rayutil import is_number


#主要程序部分
print ("是否使能动态端口(y/n)")
dp=raw_input()
if dp == 'y' or dp == 'Y':
    writejson.EnDynPort(1)
elif dp == 'n' or dp == 'N':
    writejson.EnDynPort(0)
else:
    print ("输入错误，请检查是否为数字")