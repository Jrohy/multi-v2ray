#!/usr/bin/env python3
# coding: utf-8


import re
import string

from .colored_string import ColoredString

listtype = (tuple, list)

invisible_chars = ''.join(map(chr, list(range(0, 32))))
invisible_chars_re = re.compile('[%s]' % re.escape(invisible_chars))


def _findquote(line, quote):
    if len(quote) == 0:
        return -1, -1, []

    i = 0
    n = len(line)
    escape = []
    while i < n:
        if line[i] == '\\':
            escape.append(i)
            i += 2
            continue

        if line[i] in quote:
            quote_s = i - len(escape)

            j = i
            i += 1
            while i < n and line[i] != line[j]:
                if line[i] == '\\':
                    escape.append(i)
                    i += 2
                    continue

                i += 1

            if i < n:
                quote_e = i - len(escape)
                return quote_s, quote_e, escape
            else:
                return quote_s, -1, escape

        i += 1

    return -1, -1, escape


def parse_colon_kvs(data):
    data = tokenize(data, quote='"\'')

    ret = {}
    for buf in data:
        if ':' not in buf:
            raise ValueError('invalid arguments, arguments'
                             'need key-val like: "k:v"')

        k, v = buf.split(':', 1)

        ret[k] = v

    return ret


def tokenize(line, sep=None, quote='"\'', preserve=False):
    if sep == quote:
        raise ValueError('diffrent sep and quote is required')

    if sep is None:
        if len(line) == 0:
            return []
        line = line.strip()

    rst = ['']
    n = len(line)
    i = 0
    while i < n:
        quote_s, quote_e, escape = _findquote(line[i:], quote)

        if len(escape) > 0:
            lines = []
            x = 0
            for e in escape:
                lines.append(line[x:i + e])
                x = i + e + 1
            lines.append(line[x:])
            line = ''.join(lines)
            n = len(line)

        if quote_s < 0:
            sub = n
        else:
            sub = i + quote_s

        if i < sub:
            sub_rst = line[i:sub].split(sep)
            if sep is None:
                if line[sub - 1] in string.whitespace:
                    sub_rst.append('')
                if line[i] in string.whitespace:
                    sub_rst.insert(0, '')

            head = rst.pop()
            sub_rst[0] = head + sub_rst[0]
            rst += sub_rst

        if quote_s < 0:
            break

        # discard incomplete
        # 'a b"c'  ->  ['a']
        if quote_e < 0:
            rst.pop()
            break

        head = rst.pop()

        if preserve:
            head += line[i + quote_s:i + quote_e + 1]
        else:
            head += line[i + quote_s + 1:i + quote_e]

        rst.append(head)
        i += quote_e + 1

    return rst


def line_pad(linestr, padding=''):

    lines = linestr.split("\n")

    if type(padding) == str:
        lines = [padding + x for x in lines]

    elif callable(padding):
        lines = [padding(x) + x for x in lines]

    lines = "\n".join(lines)

    return lines


def format_line(items, sep=' ', aligns=''):
    '''
    format a line with multi-row columns.

        items = [ 'name:',
                  [ 'John',
                    'j is my nick'
                  ],
                  [ 'age:' ],
                  [ 26, ],
                  [ 'experience:' ],
                  [ '2000 THU',
                    '2006 sina',
                    '2010 other'
                  ],
        ]

        format_line(items, sep=' | ', aligns = 'llllll')

    outputs:

        name: | John         | age: | 26 | experience: | 2000 THU
              | j is my nick |      |    |             | 2006 sina
              |              |      |    |             | 2010 other

    '''

    aligns = [x for x in aligns] + [''] * len(items)
    aligns = aligns[:len(items)]
    aligns = ['r' if x == 'r' else x for x in aligns]

    items = [(x if type(x) in listtype else [x])
             for x in items]

    items = [[_to_str(y)
              for y in x]
             for x in items]

    maxHeight = max([len(x) for x in items] + [0])

    def max_width(x): return max([y.__len__()
                                  for y in x] + [0])

    widths = [max_width(x) for x in items]

    items = [(x + [''] * maxHeight)[:maxHeight]
             for x in items]

    lines = []
    for i in range(maxHeight):
        line = []
        for j in range(len(items)):
            width = widths[j]
            elt = items[j][i]

            actualWidth = elt.__len__()

            if actualWidth < width:
                padding = ' ' * (width - actualWidth)
                if aligns[j] == 'l':
                    elt = elt + padding
                else:
                    elt = padding + elt

            line.append(elt)

        line = sep.join(line)

        lines.append(line)

    return "\n".join(lines)


def struct_repr(data, key=None):
    '''
    Render a data to a multi-line structural(yaml-like) representation.

        a = {
                1: 3,
                'x': {1:4, 2:5},
                'l': [1, 2, 3],
        }
        for l in struct_repr(a):
            print l

    Output:

        1 : 3
        l : - 1
            - 2
            - 3
        x : 1 : 4
            2 : 5
    '''

    if type(data) in listtype:

        if len(data) == 0:
            return ['[]']

        max_width = 0
        elt_lines = []
        for elt in data:
            sublines = struct_repr(elt)
            sublines_max_width = max([len(x) for x in sublines])

            if max_width < sublines_max_width:
                max_width = sublines_max_width

            elt_lines.append(sublines)

        lines = []
        for sublines in elt_lines:

            # - subline[0]
            #   subline[1]
            #   ...

            lines.append('- ' + sublines[0].ljust(max_width))

            for l in sublines[1:]:
                lines.append('  ' + l.ljust(max_width))

        return lines

    elif type(data) == dict:

        if len(data) == 0:
            return ['{}']

        max_k_width = 0
        max_v_width = 0

        kvs = []

        for k, v in list(data.items()):
            sublines = struct_repr(v)
            sublines_max_width = max([len(x) for x in sublines])

            if max_k_width < len(k):
                max_k_width = len(k)

            if max_v_width < sublines_max_width:
                max_v_width = sublines_max_width

            kvs.append((k, sublines))

        kvs.sort(key=key)

        lines = []
        for k, sublines in kvs:

            # foo : sub-0
            #       sub-1
            #   b : sub-0
            #       sub-0

            lines.append(k.rjust(max_k_width) + ' : ' +
                         sublines[0].ljust(max_v_width))

            for l in sublines[1:]:
                lines.append(' '.rjust(max_k_width) +
                             '   ' + l.ljust(max_v_width))

        return lines

    else:

        data = filter_invisible_chars(data)
        return [data]


def _get_key_and_headers(keys, rows):

    if keys is None:

        if len(rows) == 0:
            keys = []
        else:
            r0 = rows[0]

            if type(r0) == dict:
                keys = list(r0.keys())
                keys.sort()
            elif type(r0) in listtype:
                keys = [i for i in range(len(r0))]
            else:
                keys = ['']

    _keys = []
    column_headers = []

    for k in keys:

        if type(k) not in listtype:
            k = [k, k]

        _keys.append(k[0])
        column_headers.append(str(k[1]))

    return _keys, column_headers


def _get_colors(colors, col_n):

    if colors is None:
        colors = []

    colors = colors or ([None] * col_n)

    while len(colors) < col_n:
        colors.extend(colors)

    colors = colors[:col_n]

    return colors


def format_table(rows,
                 keys=None,
                 colors=None,
                 sep=' | ',
                 row_sep=None):

    keys, column_headers = _get_key_and_headers(keys, rows)
    colors = _get_colors(colors, len(keys))

    # element of lns is a mulit-column line
    # lns = [
    #         # line 1
    #         [
    #                 # column 1 of line 1
    #                 ['name:', # row 1 of column 1 of line 1
    #                  'foo',   # row 2 of column 1 of line 1
    #                 ],
    #
    #                 # column 2 of line 1
    #                 ['school:',
    #                  'foo',
    #                  'bar',
    #                 ],
    #         ],
    # ]

    # headers
    lns = [
        [[a + ': ']
         for a in column_headers]
    ]

    for row in rows:

        if row_sep is not None:
            lns.append([[None] for k in keys])

        if type(row) == dict:

            ln = [struct_repr(row.get(k, ''))
                  for k in keys]

        elif type(row) in listtype:

            ln = [struct_repr(row[int(k)])
                  if len(row) > int(k) else ''
                  for k in keys]

        else:
            ln = [struct_repr(row)]

        lns.append(ln)

    def get_max_width(cols): return max([len(c[0]) for c in cols] + [0])

    max_widths = [get_max_width(cols) for cols in zip(*lns)]

    rows = []
    for row in lns:

        ln = []

        for i in range(len(max_widths)):
            color = colors[i]
            w = max_widths[i]

            ln.append([ColoredString(x.ljust(w), color)
                       if x is not None else row_sep * w
                       for x in row[i]])

        rows.append(format_line(ln, sep=sep))

    return rows


def filter_invisible_chars(data):
    if type(data) not in (bytes, str):
        return data

    return invisible_chars_re.sub('', data)


def _to_str(y):
    if isinstance(y, ColoredString):
        pass
    elif type(y) == type(0):
        y = str(y)
    elif type(y) in (type([]), type(()), type({})):
        y = str(y)

    return y


def common_prefix(a, *others, **options):

    recursive = options.get('recursive', True)
    for b in others:
        if type(a) != type(b):
            raise TypeError('a and b has different type: ' + repr((a, b)))
        a = _common_prefix(a, b, recursive)

    return a


def _common_prefix(a, b, recursive=True):

    rst = []
    for i, elt in enumerate(a):
        if i == len(b):
            break

        if type(elt) != type(b[i]):
            raise TypeError('a and b has different type: ' + repr((elt, b[i])))

        if elt == b[i]:
            rst.append(elt)
        else:
            break

    # Find common prefix of the last different element.
    #
    # string does not support nesting level reduction. It infinitely recurses
    # down.
    # And non-iterable element is skipped, such as int.
    i = len(rst)
    if recursive and i < len(a) and i < len(b) and not isinstance(a, str) and hasattr(a[i], '__len__'):

        last_prefix = _common_prefix(a[i], b[i])

        # discard empty tuple, list or string
        if len(last_prefix) > 0:
            rst.append(last_prefix)

    if isinstance(a, tuple):
        return tuple(rst)
    elif isinstance(a, list):
        return rst
    else:
        return ''.join(rst)


def break_line(linestr, width):
    lines = linestr.splitlines()
    rst = []

    space = ' '
    if isinstance(linestr, ColoredString):
        space = ColoredString(' ')

    for line in lines:
        words = line.split(' ')

        buf = words[0]
        for word in words[1:]:
            if len(word) + len(buf) + 1 > width:
                rst.append(buf)
                buf = word
            else:
                buf += space + word

        if buf != '':
            rst.append(buf)

    return rst
