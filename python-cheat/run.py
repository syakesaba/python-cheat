# -*- coding: utf-8 -*-
import os
import sys

from .debugger import Debugger

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

        rlcompleter.readline.parse_and_bind("tab: complete")  # TODO: multi arch
        rlcompleter.readline.read_history_file(pyhistfile)
        rlcompleter.readline.set_history_length(100)
        atexit.register(rlcompleter.readline.write_history_file, pyhistfile)
    except:
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
