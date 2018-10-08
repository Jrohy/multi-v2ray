#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from loader import Loader

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
        self.group = self.group_list[0]
        self.client_index = 0
        if self.list_size > 1: 
            self.select_client()

    def select_client(self):
        print(self.profile)
        self.group = None
        choice = input("请输入要{}的节点序号数字: ".format(self.action))

        if not choice.isnumeric():
            print('输入错误，请检查是否为数字')
            return

        choice = int(choice)
        if choice < 1 or choice > self.list_size:
            print('输入错误，请检查是否符合范围中')
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
        self.list_size = len(self.group_list)
        self.group = self.group_list[0]
        if self.list_size > 1:
            self.select_group()          

    def select_group(self):
        print(self.profile)
        choice = input("请输入要{}的节点Group字母: ".format(self.action)).upper()
        if len(choice) != 1 or not choice.isalpha() or choice > self.group_list[-1].tag:
            print('输入有误，请检查是否为字母且范围中')
            self.group = None
        else:
            self.group = [x for x in self.group_list if x.tag == choice][0]