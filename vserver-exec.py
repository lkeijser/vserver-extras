#!/usr/bin/env python

"""
    small script to quickly run commands in all vservers

    L.S. Keijser <leon@gotlinux.nl>

"""

import os
import subprocess
import sys
from optparse import OptionParser, OptionGroup


# set up option parser
parser = OptionParser(usage="%prog [-n <node> | --all] -c '<command> <arg> <arg>' [--debug]",version="%prog " + "0.1")

# populate parser
parser.add_option("-D", "--debug",
        action="count",
        dest="debug",
        help="enable debugging output")
parser.add_option("-n", "--node",
        action="store",
        dest="node",
        help="name of vserver node")
parser.add_option("-c", "--command",
        action="store",
        dest="command",
        help="command to be executed (between quotes if args are supplied)")
parser.add_option("-A", "--all",
        action="store_true",
        dest="all",
        help="process all vservers")

# parse cmd line options
(options, args) = parser.parse_args()


# check for required args
if not options.command:
    parser.error("missing required parameter: command")
if not options.node:
    if not options.all:
        parser.error("you have to specify a node or use --all")

# functions
def list_running():
    cmd = 'vserver-stat'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output = p.stdout.readlines()
    del output[0]
    vservers = []
    for i in output:
        vs = i.split()[-1]
        vservers.append(vs)
    # return all vservers in a list
    return vservers

# do the magic
if options.all:
    for vserver in list_running():
        vs_cmd = '/usr/sbin/vserver %s exec %s' % (vserver,options.command)
        if options.debug: print "\033[1;34m[DEBUG]\033[1;m\t\trunning command on %s: \033[1;37m%s\033[1;m" % (vserver,options.command)
        p = subprocess.Popen(vs_cmd, stdout=subprocess.PIPE, shell=True)
        for o in p.stdout.readlines():
            print "\033[1;30m[%s]\033[1;m\t%s" % (vserver,o.rstrip())
        print "---"
else:
    vs_cmd = '/usr/sbin/vserver %s exec %s' % (options.node,options.command)
    if options.debug: print "\033[1;34m[DEBUG]\033[1;m\t\trunning command on %s: \033[1;37m%s\033[1;m" % (options.node,options.command)
    p = subprocess.Popen(vs_cmd, stdout=subprocess.PIPE, shell=True)
    for o in p.stdout.readlines():
        print "\033[1;30m[%s]\033[1;m\t%s" % (options.node,o.rstrip())
    print "---"


