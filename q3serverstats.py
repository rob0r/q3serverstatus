#!/usr/bin/env python
__doc__ = '''
q3serverstats.py
    Author      - rob0r - github.com/rob0r
    wrapper for pyquake3.py to make probing
    quake3 servers easy. Allows loading multiple
    servers from a config file
'''

from pyquake3 import *
import argparse
import os

def connect(server,password):
    try:
        q = PyQuake3(server, password)
        return q
    except:
        print 'Failed to connect!'
        quit(1)

def printserverinfo(qcon):
    q = qcon
    q.update()
    print '%s : %s : %s : %s player(s).' % \
    (q.get_address(), q.vars['sv_hostname'], q.vars['mapname'], len(q.players))    

def printplayerinfo(qcon):
    q = qcon
    try:
        q.rcon_update()
    except:
        print 'Failed to get player info! Wrong password for ' + q.get_address()
    for player in q.players:
        print '     |-%s : %s frags : %sms ping : %s ' % \
        (player.name, player.frags, player.ping, player.address)

cliopts = argparse.ArgumentParser('Quake3 server stats')
cliopts.add_argument(
    '--server',
    default = None,
    help = 'server ip:port or hostname:port',
    type = str
    )
cliopts.add_argument(
    '--password',
    default = None,
    help = 'server rcon password',
    type = str
    )
cliopts.add_argument(
    '--config',
    default = 'config.py',
    help = 'path to config file',
    type = str
    )
cliargs = cliopts.parse_args()

# cli arguments take preference over config file
if not cliargs.server:
    if os.path.isfile(cliargs.config):
        config = open(cliargs.config)
        from config import *
        for server in servers:
            password = servers[server]
            q = connect(server,password)
            printserverinfo(q)
            printplayerinfo(q)
    else:
        print 'No config or server specified!'
elif cliargs.server and cliargs.password:
    q = connect(cliargs.server, cliargs.password)
    printserverinfo(q)
    printplayerinfo(q)
else:
    print 'server and password required!'