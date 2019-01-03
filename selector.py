#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from loader import Loader
from utils import ColorStr

class CommonSelector:
    def __init__(self, collection, msg):
        from collections.abc import Iterable
        if isinstance(collection, Iterable):
            self.collection = collection
        else:
            raise ValueError("{} 对象不可迭代".format(collection))
        self.msg = msg
    
    def select(self):
        for index, element in enumerate(self.collection):
            print("{0}.{1}".format(index + 1, element))
        choice = input(self.msg)

        if not choice.isnumeric():
            raise RuntimeError('输入错误，请检查是否为数字')

        choice = int(choice)
        if choice < 1 or choice > len(self.collection):
            raise RuntimeError('输入错误，请检查是否符合范围中')
        else:
            return self.collection[choice - 1]

class Selector:
    def __init__(self, action):
        loader = Loader()
        self.profile = loader.profile
        self.group_list = loader.profile.group_list
        self.action = action

class ClientSelector(Selector):
    def __init__(self, action):
        super(ClientSelector, self).__init__(action)
        self.list_size = self.group_list[-1].node_list[-1].user_number
        if "删除" in action and self.list_size == 1:
            print(ColorStr.red("仅剩最后一个节点无法删除!!!"))
            self.group = None
        elif self.list_size > 1: 
            self.select_client()
        else:
            self.group = self.group_list[0]
            self.client_index = 0

    def select_client(self):
        print(self.profile)
        self.group = None
        choice = input("请输入要{}的节点序号数字: ".format(self.action))

        if not choice.isnumeric():
            print(ColorStr.red('输入错误，请检查是否为数字'))
            return

        choice = int(choice)
        if choice < 1 or choice > self.list_size:
            print(ColorStr.red('输入错误，请检查是否符合范围中'))
        else:
            find = False
            for group in self.group_list:
                if find:
                    break
                for index, node in enumerate(group.node_list):
                    if node.user_number == choice:
                        self.client_index = index
                        self.group = group
                        find = True
                        break

class GroupSelector(Selector):
    def __init__(self, action):
        super(GroupSelector, self).__init__(action)
        if "删除" in action and len(self.group_list) == 1:
            print(ColorStr.red("仅剩最后一个端口无法删除!!!"))
            self.group = None
        elif len(self.group_list) > 1:
            self.select_group()
        else:
            self.group = self.group_list[0]

    def select_group(self):
        print(self.profile)
        choice = input("请输入要{}的节点Group字母: ".format(self.action))
        group_list = [x for x in self.group_list if x.tag == choice]
        if len(group_list) == 0:
            print(ColorStr.red('输入有误，请检查 {} Group是否存在'.format(choice)))
            self.group = None
        else:
            self.group = group_list[0]