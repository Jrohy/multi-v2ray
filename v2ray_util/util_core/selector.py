#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .loader import Loader
from .utils import ColorStr, readchar

class CommonSelector:
    def __init__(self, collection, msg):
        from collections.abc import Iterable
        if isinstance(collection, Iterable):
            self.collection = collection
        else:
            raise ValueError("{} object can't iterate".format(collection))
        self.msg = msg
    
    def select(self):
        for index, element in enumerate(self.collection):
            print("{0}.{1}".format(index + 1, element))

        if len(self.collection) < 10:
            choice = readchar(self.msg)                
        else:
            choice = input(self.msg)

        if not choice:
            print("use {}".format(self.collection[0]))
            return self.collection[0]

        if not choice.isnumeric():
            raise RuntimeError(_('input error, please check is number'))

        choice = int(choice)
        if choice < 1 or choice > len(self.collection):
            raise RuntimeError(_('input error, input index out of range'))
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
        if _("del") in action and self.list_size == 1:
            print(ColorStr.red(_("last node can't delete!!!")))
            self.group = None
        elif self.list_size > 1: 
            self.select_client()
        else:
            self.group = self.group_list[0]
            self.client_index = 0

    def select_client(self):
        print(self.profile)
        self.group = None
        if self.list_size < 10:
            choice = readchar("{} {}: ".format(_("please input number to"), self.action))
        else:
            choice = input("{} {}: ".format(_("please input number to"), self.action))

        if not choice:
            return
        if not choice.isnumeric():
            print(ColorStr.red(_('input error, please check is number')))
            return

        choice = int(choice)
        if choice < 1 or choice > self.list_size:
            print(ColorStr.red(_('input out of range!!')))
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
        if _("del") in action and len(self.group_list) == 1:
            print(ColorStr.red(_("last group can't delete!!!")))
            self.group = None
        elif len(self.group_list) > 1:
            self.select_group()
        else:
            self.group = self.group_list[0]

    def select_group(self):
        print(self.profile)
        if len(self.group_list[-1].tag) == 1:
            choice = readchar("{} {}: ".format(_("please input group to"), self.action))
        else:
            choice = input("{} {}: ".format(_("please input group to"), self.action))
        group_list = [x for x in self.group_list if x.tag == str.upper(choice)]
        if len(group_list) == 0:
            print(ColorStr.red('{0} {1} {2}'.format(_("input error, please check group"), choice, _("exist"))))
            self.group = None
        else:
            self.group = group_list[0]