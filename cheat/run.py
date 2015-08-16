# -*- coding: utf-8 -*-
import os
import sys

from debugger import Debugger

if __name__ == '__main__':
    if os.getuid() != 0:
        print "Run as root"
        print "sudo python -m python-cheat.run <pid> [<pid> ...]"
        sys.exit(-1)

    if len(sys.argv) < 2:
        print "sudo python -m python-cheat.run <pid> [<pid> ...]"
        sys.exit(-1)

    cheater = Debugger()

    for pid in sys.argv[1:]:
        try:
            pid = int(pid)
            print "Adding %d" % pid
            cheater.addProcess(pid, False)
        except Exception as e:
            print "Invalid pid %s" % pid
            print e
            sys.exit(-1)
    try:
        import rlcompleter
        import atexit

        home = os.path.expanduser('~')
        pyhistfile = os.path.join(home, '.python-cheat')
        if not os.path.exists(pyhistfile):
            with open(pyhistfile, "w") as fp:
                fp.write("")
        if "libedit" in rlcompleter.readline.__doc__:
            #BSD with libedit
            rlcompleter.readline.parse_and_bind("bind -e")
            rlcompleter.readline.parse_and_bind("bind '\t' rl_complete")
        else:
            rlcompleter.readline.parse_and_bind("tab: complete")
        try:
            rlcompleter.readline.read_history_file(pyhistfile)
        except Exception as e:
            #First creation of history file.
            pass
        rlcompleter.readline.set_history_length(100)
        atexit.register(rlcompleter.readline.write_history_file, pyhistfile)
    except ImportError as e:
        pass

    from code import interact
    # http://pueblo.sourceforge.net/doc/manual/ansi_color_codes.html
    usage = """
    cheater.addProcess()
    cheater.deleteProcess()
    cheater.dumpRegs()
    cheater.start_target()
    cheater.stop_target()
    cheater.sqitch_target()

    Enjoy

    =====
    """
    sys.ps1 = "({pid})>>> ".format(pid=cheater.target.pid)
    interact(banner=__import__('textwrap').dedent(usage), local=locals())
