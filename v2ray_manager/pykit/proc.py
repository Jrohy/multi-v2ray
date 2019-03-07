#!/usr/bin/env python3
# coding: utf-8

import errno
import logging
import os

import subprocess32

logger = logging.getLogger(__name__)


class ProcError(Exception):

    def __init__(self, returncode, out, err, cmd, arguments, options):

        super(ProcError, self).__init__(returncode,
                                        out,
                                        err,
                                        cmd,
                                        arguments,
                                        options)

        self.returncode = returncode
        self.out = out
        self.err = err
        self.command = cmd
        self.arguments = arguments
        self.options = options


def command(cmd, *arguments, **options):

    close_fds = options.get('close_fds', True)
    cwd = options.get('cwd', None)
    shell = options.get('shell', False)
    env = options.get('env', None)
    if env is not None:
        env = dict(os.environ, **env)
    stdin = options.get('stdin', None)

    subproc = subprocess32.Popen([cmd] + list(arguments),
                                 close_fds=close_fds,
                                 shell=shell,
                                 cwd=cwd,
                                 env=env,
                                 stdin=subprocess32.PIPE,
                                 stdout=subprocess32.PIPE,
                                 stderr=subprocess32.PIPE, )

    out, err = subproc.communicate(input=stdin)

    subproc.wait()

    return (subproc.returncode, out, err)


def command_ex(cmd, *arguments, **options):
    returncode, out, err = command(cmd, *arguments, **options)
    if returncode != 0:
        raise ProcError(returncode, out, err, cmd, arguments, options)

    return returncode, out, err


def shell_script(script_str, **options):
    options['stdin'] = script_str
    return command('bash', **options)
