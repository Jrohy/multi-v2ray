#!/usr/bin/env python3
# coding: utf-8

import cmd
import getopt
import os
import readline
import sys
import time
import traceback

import cmdutil
import mgrcmds
from pykit import modutil
from pykit import strutil

readline.set_completer_delims('     `~!@#$%^&*()=+[{]}\|;:",<>/?' + "'")

runtime_prompt = lambda : '[{name} {now}]$ '.format(
                    name=strutil.ColoredString(
                        'v2ray', color='green', prompt=True),
                    now=time.strftime('%H:%M:%S',
                        time.localtime(time.time().__int__())),
                    )

class Managecmd(cmd.Cmd):

    prompt = runtime_prompt()

    def get_names(self):

        return [k for k in dir(self)]

    def __init__(self, cmdqueue=[]):

        cmd.Cmd.__init__(self)

        self.stop = False
        self.cmdqueue = cmdqueue
        self.load_external_cmd()

    def load_external_cmd(self):

        mods = modutil.submodules(mgrcmds)

        for n, mod in list(mods.items()):
            if not n.startswith('cmd_'):
                continue

            n = n[len('cmd_'):]

            try:
                setattr(self, 'complete_' + n, mod.complete)
            except AttributeError:
                setattr(self, 'complete_' + n,
                         cmdutil.build_completer_by_dict(mod.subcmd))

            setattr(self, 'do_' + n, mod.doit)

    def cmdloop(self, intro=None):

        while not self.stop:
            self.prompt = runtime_prompt()
            try:
                cmd.Cmd.cmdloop(self)
            except KeyboardInterrupt:
                cmdutil.message('')

    def onecmd(self, line):
        """Interpret the argument as though it had been typed in response
        to the prompt.

        This may be overridden, but should not normally need to be;
        see the precmd() and postcmd() methods for useful execution hooks.
        The return value is a flag indicating whether interpretation of
        commands by the interpreter should stop.

        """

        self.prompt = runtime_prompt()

        cmd, arg, line = self.parseline(line)
        if not line:
            return
        if cmd == '':
            return self.default(line)

        try:
            func = getattr(self, 'do_' + cmd)
        except AttributeError:
            return self.default(line)

        try:
            return func(arg)
        except Exception as e:
            try:
                self._except(e)
            except Exception:
                traceback.print_exc()
                return

    def _except(self, e):

        clz = e.__class__

        if clz == cmdutil.UnknownCommand:
            cmdutil.message('Invalid command:', ' '.join(e.args))

        elif clz == cmdutil.InvalidArgument:
            cmdutil.message('Invalid argument:', repr(e))

        elif clz == cmdutil.HelpOnly:
            pass

        else:
            raise

    def do_exit(self, argv):
        self.stop = True
        return True

    def do_shell(self, argv):
        os.system(argv)


if __name__=='__main__':

    opts, argv = getopt.getopt( sys.argv[1:] , 'e:c:', ['nocolor',] )
    opts = dict(opts)

    if '-e' in opts :
        dictate = opts['-e'].split(';') + ['exit',]
    else :
        dictate = []

    mcmd = Managecmd(dictate)
    mcmd.cmdloop()
