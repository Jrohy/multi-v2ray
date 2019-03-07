#!/usr/bin/env python3
# coding: utf-8

import datetime
import os

from . import cmdopt
from . import managersession
from ..pykit import strutil

class CmdutilError(Exception): pass
class HelpOnly(CmdutilError ): pass
class UnknownCommand(CmdutilError): pass
class InvalidArgument(CmdutilError): pass

class Command(object):

    def __init__(self, parser, worker):

        if type(parser) in (list, tuple):
            parser = cmdopt.build_parser(parser)

        self.parser = parser
        self.worker = worker

    def options(self):
        opts = self.parser.option_list
        return [x._long_opts[0] for x in opts]


def getinput(prompt, acceptinput=lambda x: True):

    try:
        '1' in acceptinput
        acpt_func = lambda x: x in acceptinput
    except:
        acpt_func = acceptinput

    while True:
        try :
            r = input(prompt).strip()
            if acpt_func(r):
                break

        except KeyboardInterrupt:
            r = None
            print()

    return r


def build_completer_by_dict(subcmd):
    def _complete(text, line, s, e):
        return complete_by_dict(subcmd, text, line, s, e)

    return _complete


def complete_by_dict(dic, text, line, s, e):

    argstr = line[:s]

    arglist = strutil.tokenize(argstr, quote='"\'')

    for i in range(len(arglist)):
        if arglist[i].startswith('-'):
            arglist = arglist[:i]
            break

    arglist = arglist[1:]

    node = dic

    for k in arglist:
        if type(node) == dict and k in node:
            node = node[k]

    if type(node) == dict:
        if text in node:
            return [text + ' ']
        else:
            cmpl = [x + ' ' for x in list(node.keys())
                     if x.startswith(text) and x != '__shortcut__']

            if '__shortcut__' in node:
                cmd = _get_shortcut_cmd(dic)

                opts = cmd.options()
                cmpl += [x + ' ' for x in opts if x.startswith(text)]

            return cmpl

    elif isinstance(node, Command):
        # opts are list of long-options with leading "-"
        opts = node.options()
        r = [x + ' ' for x in opts if x.startswith(text)]

        return r

    elif type(node) == tuple:
        # option

        r = []
        for opts in node:

            # NOTE: Cmd does not recognize '--' as valid char, thus we must
            # not prepend '--' to option strings

            if type(opts) == dict:
                # short-long mapping options
                r.extend([x + ' ' for x in list(opts.values())
                            if ('--' + x).startswith(text)])

            elif type(opts) == list:
                # long option
                r.extend([x + ' ' for x in opts
                            if ('--' + x).startswith(text)])
        return r

    else:
        return []


def run_std_sub_command(subcmd, argstr):
    cmds, c, uconf, params = get_std_sub_command(subcmd, argstr)
    if uconf.get('help'):
        print(c.parser.format_help())
    else:
        c.worker(cmds, uconf, params)


def sess_data(x):
    if x.startswith('$') and x in managersession.userSessData:
        return managersession.userSessData[x]
    return [x]


def get_std_sub_command(subcmd, argstr, printHelp=False):

    # accept only Command instance.

    rawparams = strutil.tokenize(argstr, quote='"\'')

    cmds, c, params = match_command(subcmd, rawparams)

    try:
        uconf, params = c.parser.parse_args(params)
    except cmdopt.ParserError as e:
        message("")
        message(e[ 0 ])
        message("")
        message(c.parser.format_help())

        raise HelpOnly()

    params = sum([sess_data(x) for x in params], [])

    uconf = uconf.__dict__.copy()

    if printHelp and uconf.get('help'):
        print(c.parser.format_help())

        raise HelpOnly()

    return cmds, c, uconf, params

def _get_shortcut_cmd(node):

    shortcut = node['__shortcut__'].split('.')

    cmd = node
    for s in shortcut:
        cmd = cmd[s]

    return cmd

def match_command(dic, params, mode='cmdonly'):

    cmds = []

    if params == [] and '__shortcut__' in dic:
        cmd = _get_shortcut_cmd(dic)
        return cmds, cmd, params

    for c in params:

        if type(dic) == dict:

            if c in dic:
                cmds.append(c)
                dic = dic[c]

            elif '__shortcut__' in dic:
                cmd = _get_shortcut_cmd(dic)
                return cmds, cmd, params[len(cmds):]

            else:
                raise UnknownCommand(*params)
        else:
            break

    if dic is True or callable(dic) or isinstance(dic, Command):
        return cmds, dic, params[len(cmds):]

    elif type(dic) == tuple:
        # options of a valid command
        for e in dic:
            if e is True or callable(e):
                if mode == 'cmdonly':
                    return cmds, e, params[len(cmds):]
                elif mode == 'withopt':
                    return cmds, dic, params[len(cmds):]
                else:
                    return cmds, e, params[len(cmds):]

        else:
            raise UnknownCommand(*params)

    else:
        raise UnknownCommand(*params)


def message(*msgs):
    s = ' '.join( msgs ) + "\n"
    os.write(1, s.encode('utf-8'))
