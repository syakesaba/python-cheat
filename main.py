#!/usr/bin/env python
# encoding: utf-8

import ptrace
import sys
import os

from cheat import CheatDebugger

if __name__ == "__main__":
    if os.getuid() != 0:
        print "Run as root"
        print "sudo",__file__,"<pid> [<pid> ...]"
        exit(-1)
    if len(sys.argv) < 2:
        print __file__," <pid> [<pid> ...]"
        exit(-1)
    cheater = CheatDebugger()
    for pid in sys.argv[1:]:
        try:
            pid = int(pid)
            print "Adding %d" % pid
            cheater.addProcess(pid,False)
        except Exception as e:
            print "Invalid pid %s" % pid
            print e
            exit(-1)
    try:
        import rlcompleter,atexit
        home = os.path.expanduser('~')
        pyhistfile = os.path.join(home, '.python-cheat')
        if not os.path.exists(pyhistfile):
            f = open(pyhistfile,"w")
            f.write("")
            f.close()
        rlcompleter.readline.parse_and_bind("tab: complete") #TODO: multi arch
        rlcompleter.readline.read_history_file(pyhistfile)
        rlcompleter.readline.set_history_length(100)
        atexit.register(rlcompleter.readline.write_history_file, pyhistfile)
    except:
        pass
    from code import interact
    #http://pueblo.sourceforge.net/doc/manual/ansi_color_codes.html
    usage=\
"""
cheater.addProcess()
cheater.deleteProcess()
cheater.dumpRegs()
cheater.start_target()
cheater.stop_target()
cheater.sqitch_target()

Enjoy

====="""
    sys.ps1="(" + str(cheater.target.pid) + ") > "
    interact(banner=usage,local=locals())
