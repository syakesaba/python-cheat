from ptrace.debugger.process_error import ProcessError

class CheatRegister(object):
    def __init__(self, debugger):
        self.debugger = debugger
    def __getitem__(self, item):
        try:
            return self.debugger.target.getreg(item)
        except ProcessError:# as e:
            pass