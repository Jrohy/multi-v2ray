#!/usr/bin/env python3
# coding: utf-8

import optparse

MAX = [ '-m', '--max',
        { 'help': "max number to operate",
          'default': 10000000,
          'action': 'store',
          'type': 'int',
          'metavar': 'NUM',
        } ]

VERBOSE = [ '-v', '--verbose',
        { 'help': "output additional information",
          'default': False,
          'action': 'store_true',
        } ]

FORCE = [ '-f', '--force',
        { 'help': "force doing",
          'default': False,
          'action': 'store_true',
        } ]

YES = [ '-y', '--yes',
        { 'help': "yes to all confirmations",
          'default': False,
          'action': 'store_true',
        } ]

HELP = [ '-h', '--help',
        { 'help': "help",
          'default': False,
          'action': 'store_true',
        } ]

emptyParser = optparse.OptionParser( add_help_option=False )
emptyParser.add_option( *( HELP[ 0:2 ] ), **HELP[ 2 ] )

class ParserError( Exception ): pass

class OptionParser( optparse.OptionParser ):
    def error( self, msg ):
        raise ParserError( msg )

def build_parser( *args, **argkv ):

    usage = argkv.get( 'usage' )
    if usage is not None:
        # Format usage strings with the same indent.
        indent = ' ' * len('usage: ')
        lines = usage.split('\n')
        lines = [lines[0]] + [indent + p.strip() for p in lines[1:]]
        usage = '\n'.join(lines)

    parser = OptionParser( add_help_option=False, usage=usage )

    names, kvs = [], {}

    for a in HELP + list(args):
        if type( a ) == type( '' ):
            names.append( a )
        elif type( a ) == type( {} ):
            kvs = a
            parser.add_option( *names, **kvs )
            names, kvs = [], {}

    if names != []:
        parser.add_option( *names, **kvs )

    return parser
