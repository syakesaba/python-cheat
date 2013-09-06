#!/usr/bin/env python
# encoding: utf-8

# see http://www21.atpages.jp/sugeryouyeah/python/index.html

import ptrace.debugger # https://pypi.python.org/packages/source/p/python-ptrace/python-ptrace-0.6.5.tar.gz
import strace # cp python-ptrace-0.6.5/strace.py /usr/local/lib/python3.1/dist-packages/
import distorm3 # http://code.google.com/p/distorm/downloads/
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
        except:
            print "Invalid pid %s" % pid
            exit(-1)
    try:
        import rlcompleter,atexit
        pyhistfile=os.getenv("HOME")+"/.pyhistory"
        rlcompleter.readline.parse_and_bind("tab: complete")
        rlcompleter.readline.read_history_file(pyhistfile)
        rlcompleter.readline.set_history_length(100)
        atexit.register(rlcompleter.readline.write_history_file, pyhistfile)
        print "TAB: Complete;Saving History in '%s' " % pyhistfile
        del os,pyhistfile
    except:
        pass
    from code import interact
    sys.ps1 ="\x1B[1m\x1B[31m>\x1B[33m>\x1B[32m>\x1B[0m "
    #http://pueblo.sourceforge.net/doc/manual/ansi_color_codes.html
    usage=\
"""
cheater.addProcess()
cheater.deleteProcess()
cheater.dumpRegs()
cheater.start_target()
cheater.stop_target()
cheater.sqitch_target()
"""
    interact(banner=usage,local=locals())
