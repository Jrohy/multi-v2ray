#!/usr/bin/env python3
# coding: utf-8

import re
import string
import sys


def colorize(percent, total=100, ptn='{0}'):
    if total > 0:
        color = fading_color(percent, total)
    else:
        color = fading_color(-total - percent, -total)
    return ColoredString(ptn.format(percent), color)


class ColoredString(object):

    def __init__(self, v, color=None, prompt=True):
        if type(color) == str:
            color = _named_colors[color]

        if isinstance(v, ColoredString):
            vs = ''.join([x[0] for x in v.elts])
            self.elts = [(vs, color)]
        else:
            self.elts = [(str(v), color)]

        self._prompt = prompt

    def __str__(self):
        rst = []
        for e in self.elts:
            if len(e[0]) == 0:
                continue

            if e[1] is None:
                val = e[0]
            else:
                _clr = '\033[38;5;' + str(e[1]) + 'm'
                _rst = '\033[0m'

                if self._prompt:
                    _clr = '\001' + _clr + '\002'
                    _rst = '\001' + _rst + '\002'

                val = _clr + str(e[0]) + _rst

            rst.append(val)

        return ''.join(rst)

    def __len__(self):
        return sum([len(x[0])
                    for x in self.elts])

    def __add__(self, other):
        prompt = self._prompt
        if isinstance(other, ColoredString):
            prompt = prompt or other._prompt

        c = ColoredString('', prompt=prompt)
        if isinstance(other, ColoredString):
            c.elts = self.elts + other.elts
        else:
            c.elts = self.elts[:] + [(str(other), None)]
        return c

    def __mul__(self, num):
        c = ColoredString('', prompt=self._prompt)
        c.elts = self.elts * num
        return c

    def __eq__(self, other):
        if not isinstance(other, ColoredString):
            return False
        return str(self) == str(other) and self._prompt == other._prompt

    def _find_sep(self, line, sep):
        ma = re.search(sep, line)
        if ma is None:
            return -1, 0

        return ma.span()

    def _recover_colored_str(self, colored_chars):
        rst = ColoredString('')
        n = len(colored_chars)
        if n == 0:
            return rst

        head = list(colored_chars[0])
        for ch in colored_chars[1:]:
            if head[1] == ch[1]:
                head[0] += ch[0]
            else:
                rst += ColoredString(head[0], head[1])
                head = list(ch)
        rst += ColoredString(head[0], head[1])

        return rst

    def _split(self, line, colored_chars, sep, maxsplit, keep_sep, keep_empty):
        rst = []
        n = len(line)
        i = 0
        while i < n:
            if maxsplit == 0:
                break

            s, e = self._find_sep(line[i:], sep)

            if s < 0:
                break

            edge = s
            if keep_sep:
                edge = e

            rst.append(self._recover_colored_str(colored_chars[i:i + edge]))

            maxsplit -= 1
            i += e

        if i < n:
            rst.append(self._recover_colored_str(colored_chars[i:]))

        # sep in the end
        # 'a b '  ->  ['a', 'b', '']
        elif keep_empty:
            rst.append(ColoredString(''))

        return rst

    def _separate_str_and_colors(self):
        colored_char = []
        line = ''
        for elt in self.elts:
            for c in elt[0]:
                colored_char.append((c, elt[1]))
            line += elt[0]

        return line, colored_char

    def splitlines(self, *args):
        # to verify arguments
        ''.splitlines(*args)

        sep = '\r(\n)?|\n'
        maxsplit = -1
        keep_empty = False
        keep_sep = False
        if len(args) > 0:
            keep_sep = args[0]

        line, colored_chars = self._separate_str_and_colors()

        return self._split(line, colored_chars, sep, maxsplit, keep_sep, keep_empty)

    def split(self, *args):
        # to verify arguments
        ''.split(*args)

        sep, maxsplit = (list(args) + [None, None])[:2]
        if maxsplit is None:
            maxsplit = -1
        keep_empty = True
        keep_sep = False

        line, colored_chars = self._separate_str_and_colors()

        i = 0
        if sep is None:
            sep = '\s+'
            keep_empty = False

            # to skip whitespaces at the beginning
            # ' a b'.split() -> ['a', 'b']
            n = len(line)
            while i < n and line[i] in string.whitespace:
                i += 1

        return self._split(line[i:], colored_chars[i:], sep, maxsplit, keep_sep, keep_empty)

    def join(self, iterable):
        rst = ColoredString('')
        for i in iterable:
            if len(rst) == 0:
                rst += i
            else:
                rst += self + i
        return rst


def fading_color(v, total):
    return _clrs[_fading_idx(v, total)]


def _fading_idx(v, total=100):
    l = len(_clrs)
    pos = int(v * l / (total + 0.0001) + 0.5)
    pos = min(pos, l - 1)
    pos = max(pos, 0)
    return pos


_clrs = [63, 67, 37, 36, 41, 46, 82, 118,
         154, 190, 226, 220, 214, 208, 202, 196]

_named_colors = {
    # by emergence levels
    'danger': _clrs[_fading_idx(100)],
    'warn': 3,
    'loaded': _clrs[_fading_idx(30)],
    'normal': 7,
    'optimal': _clrs[_fading_idx(0)],

    'dark': _clrs[1],

    # for human
    'blue': 67,
    'cyan': 37,
    'green': 46,
    'yellow': 226,
    'red': 196,
    'purple': 128,
    'white': 255,
}


def _make_colored_function(name):
    def _colored(v):
        return ColoredString(v, name)

    _colored.__name__ = name

    return _colored


for _func_name in _named_colors:
    setattr(sys.modules[__name__],
            _func_name, _make_colored_function(_func_name))
