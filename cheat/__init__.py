#!/usr/bin/env python
# encoding: utf-8

#nitePRっぽくしたい。

import ptrace.debugger
import strace # cp python-ptrace-0.6.5/strace.py /usr/local/lib/python3.1/dist-packages/
import distorm3 # http://code.google.com/p/distorm/downloads/
from functools import wraps
import os

def pidof(pid):
    os.system("pidof %d" % pid)

from cheatMemory import CheatMemory
from cheatRegister import CheatRegister

from ptrace.debugger.process_error import ProcessError,PtraceError

class CheatDebugger(ptrace.debugger.PtraceDebugger):

    def __init__(self):
        ptrace.debugger.PtraceDebugger.__init__(self)
        self._target_process = None

    @classmethod
    def lock_it(cls,f):
        @wraps(f)
        def StartExecRestart(self, *args, **keys):
            self.stop_target()
            f(*args, **keys)
            self.start_target()
        return StartExecRestart

    @property
    def target(self):
        return self._target_process

    @target.setter
    def target(self, targette):
        self._target_process = targette

    def addProcess(self, pid, is_attached, parent=None):
        ret = ptrace.debugger.PtraceDebugger.addProcess(self, pid, is_attached, parent)
        if ret is not None and self._target_process is None:
            self._target_process = ret
        return ret
    
    def deleteProcess(self, process=None, pid=None):
        ret = ptrace.debugger.PtraceDebugger.deleteProcess(self, process, pid)
        if self._target_process is not None:
            if process is not None and self._target_process.pid == process.pid or\
                pid is not None and self._target_process.pid == pid:
                if self.list:
                    self._target_process = self.list[0]
                else:
                    self._target_process = None
        return ret
    
    def switch_target(self, target_pid):
        self._target_process = self[self.target_pid]

    def start_target(self):
        self._target_process.cont()

    def stop_target(self):
        self._target_process.kill(19)

    def show_target(self):
        self._target_process.pid

    def searchString(self, s):
        matchings = set()
        try:
            self.target.getInstrPointer()
        except ProcessError:
            self.stop_target()
        except PtraceError:
            self.stop_target()
        for mappings in self.target.readMappings():
            for matching in mappings.search(s):
                matchings.add(matching)
        self.start_target()
        return matchings

if __name__ == "__main__":
    d = CheatDebugger()
    d.addProcess(int(raw_input("pid:")), False)
    d.target.dumpRegs()
    print d.start_target()
    import time
    time.sleep(1)
    print d.stop_target()
    d.target.dumpRegs()
    time.sleep(1)
    print d.start_target()
