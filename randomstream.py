#! /usr/bin/env python
# -*- coding: utf-8 -*-
import random
import changestream

changestream.writeStreamJson(str(random.randint(5,7)))
