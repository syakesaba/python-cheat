#!/usr/bin/env python
# encoding: utf-8

#nitePRっぽくしたい。

import ptrace.debugger
import strace # cp python-ptrace-0.6.5/strace.py /usr/local/lib/python3.1/dist-packages/
import distorm3 # http://code.google.com/p/distorm/downloads/
from functools import wraps
import os
import struct
from config import SystemInfo,ProgPath

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

#searching
#Format  C Type  Python type     Standard size   Notes
#x   pad byte    no value         
#c   char    string of length 1  1    
#b   signed char     integer     1   (3)
#B   unsigned char   integer     1   (3)
#?   _Bool   bool    1   (1)
#h   short   integer     2   (3)
#H   unsigned short  integer     2   (3)
#i   int     integer     4   (3)
#I   unsigned int    integer     4   (3)
#l   long    integer     4   (3)
#L   unsigned long   integer     4   (3)
#q   long long   integer     8   (2), (3)
#Q   unsigned long long  integer     8   (2), (3)
#f   float   float   4   (4)
#d   double  float   8   (4)
#s   char[]  string       
#p   char[]  string       
#P   void *  integer         (5), (3)

    def searchString(self, s):
        matchings = []
        try:
            self.target.getInstrPointer()
        except ProcessError:
            self.stop_target()
        except PtraceError:
            self.stop_target()
        for mappings in self.target.readMappings():
            print "Searching " + str(mappings)
            for matching in mappings.search(s):
                print "matched => " + str(hex(matching))
                matchings.append(matching)
        self.start_target()
        return matchings

    def searchBool(self, b):
        return searchString(struct.pack(SystemInfo.endian+"?", b))

    def searchShort(self, s):
        return searchString(struct.pack(SystemInfo.endian+"h", s))

    def searchShortUnsigned(self, s):
        return searchString(struct.pack(SystemInfo.endian+"H", s))

    def searchInt(self, i):
        return searchString(struct.pack(SystemInfo.endian+"i", i))

    def searchIntUnsigned(self, i):
        return searchString(struct.pack(SystemInfo.endian+"I", i))

    def searchLong(self, l):
        return searchString(struct.pack(SystemInfo.endian+"l", l))

    def searchLongUnsigned(self, l):
        return searchString(struct.pack(SystemInfo.endian+"L", l))

    def searchLongLong(self, ll):
        return searchString(struct.pack(SystemInfo.endian+"q", ll))

    def searchLongLongUnsigned(self, ll):
        return searchString(struct.pack(SystemInfo.endian+"Q", ll))

    def searchFloat(self, f):
        return searchString(struct.pack(SystemInfo.endian+"f", f))

    def searchDouble(self, d):
        return searchString(struct.pack(SystemInfo.endian+"d", d))

    def searchVoid(self, p):
        return searchString(struct.pack(SystemInfo.endian+"P", p))

#Dumping-Searching
# less than, greater than, equal, diff
    def dumpAllMemory(self):
        pass
    def diffMemory(self):
        pass
# or implement in different file?

#Pythonic Searcing
    def searchMatcher(self, bytes_per_read, function):
        pass

#Pointer Searching
    def serachPointer(self):
        pass
