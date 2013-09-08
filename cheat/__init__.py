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

#============Searching Memory

    def searchString(self, s):
        matchings = set()
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
                matchings.add(matching)
        self.start_target()
        return matchings

    def searchBool(self, b):
        return self.searchString(struct.pack(SystemInfo.endian+"?", b))

    def searchShort(self, s):
        return self.searchString(struct.pack(SystemInfo.endian+"h", s))

    def searchShortUnsigned(self, s):
        return self.searchString(struct.pack(SystemInfo.endian+"H", s))

    def searchInt(self, i):
        return self.searchString(struct.pack(SystemInfo.endian+"i", i))

    def searchIntUnsigned(self, i):
        return self.searchString(struct.pack(SystemInfo.endian+"I", i))

    def searchLong(self, l):
        return self.searchString(struct.pack(SystemInfo.endian+"l", l))

    def searchLongUnsigned(self, l):
        return self.searchString(struct.pack(SystemInfo.endian+"L", l))

    def searchLongLong(self, ll):
        return self.searchString(struct.pack(SystemInfo.endian+"q", ll))

    def searchLongLongUnsigned(self, ll):
        return self.searchString(struct.pack(SystemInfo.endian+"Q", ll))

    def searchFloat(self, f):
        return self.searchString(struct.pack(SystemInfo.endian+"f", f))

    def searchDouble(self, d):
        return self.searchString(struct.pack(SystemInfo.endian+"d", d))

    def searchVoid(self, p):
        return self.searchString(struct.pack(SystemInfo.endian+"P", p))

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

#============Reading Memory

    def readBytes(self, addr, length):
        try:
            self.target.getInstrPointer()
        except ProcessError:
            self.stop_target()
        except PtraceError:
            self.stop_target()
        ret = self.target.readBytes(addr,length)
        self.start_target()
        return ret

    def readBool(self, addr):
        return struct.unpack(SystemInfo.endian + "?",self.readBytes(addr,SystemInfo.sizeof.bool))

    def readShort(self, addr):
        return struct.unpack(SystemInfo.endian + "h",self.readBytes(addr,SystemInfo.sizeof.short))

    def readShortUnsigned(self, addr):
        return struct.unpack(SystemInfo.endian + "H",self.readBytes(addr,SystemInfo.sizeof.ushort))

    def readInt(self, addr):
        return struct.unpack(SystemInfo.endian + "i",self.readBytes(addr,SystemInfo.sizeof.int))

    def readIntUnsigned(self, addr):
        return struct.unpack(SystemInfo.endian + "I",self.readBytes(addr,SystemInfo.sizeof.uint))

    def readLong(self, addr):
        return struct.unpack(SystemInfo.endian + "l",self.readBytes(addr,SystemInfo.sizeof.long))

    def readLongUnsigned(self, addr):
        return struct.unpack(SystemInfo.endian + "L",self.readBytes(addr,SystemInfo.sizeof.ulong))

    def readLongLong(self, addr):
        return struct.unpack(SystemInfo.endian + "q",self.readBytes(addr,SystemInfo.sizeof.longlong))

    def readLongLongUnsigned(self, addr):
        return struct.unpack(SystemInfo.endian + "Q",self.readBytes(addr,SystemInfo.sizeof.ulonglong))

    def readFloat(self, addr):
        return struct.unpack(SystemInfo.endian + "f",self.readBytes(addr,SystemInfo.sizeof.float))

    def readDouble(self, addr):
        return struct.unpack(SystemInfo.endian + "d",self.readBytes(addr,SystemInfo.sizeof.double))

    def readVoid(self, addr):
        return struct.unpack(SystemInfo.endian + "P",self.readBytes(addr,SystemInfo.sizeof.void))

#============Writing Memory

    def writeBytes(self, addr, data):
        try:
            self.target.getInstrPointer()
        except ProcessError:
            self.stop_target()
        except PtraceError:
            self.stop_target()
        ret = self.target.writeBytes(addr,data)
        self.start_target()
        return ret

    def writeBool(self, addr, b):
        return self.writeBytes(addr, struct.pack(SystemInfo.endian+"?", b))

    def writeShort(self, addr, s):
        return self.writeBytes(addr, struct.pack(SystemInfo.endian+"h", s))

    def writeShortUnsigned(self, addr, s):
        return self.writeBytes(addr, struct.pack(SystemInfo.endian+"H", s))

    def writeInt(self, addr, i):
        return self.writeBytes(addr, struct.pack(SystemInfo.endian+"i", i))

    def writeIntUnsigned(self, addr, i):
        return self.writeBytes(addr, struct.pack(SystemInfo.endian+"I", i))

    def writeLong(self, addr, l):
        return self.writeBytes(addr, struct.pack(SystemInfo.endian+"l", l))

    def writeLongUnsigned(self, addr, l):
        return self.writeBytes(addr, struct.pack(SystemInfo.endian+"L", l))

    def writeLongLong(self, addr, ll):
        return self.writeBytes(addr, struct.pack(SystemInfo.endian+"q", ll))

    def writeLongLongUnsigned(self, addr, ll):
        return self.writeBytes(addr, struct.pack(SystemInfo.endian+"Q", ll))

    def writeFloat(self, addr, f):
        return self.writeBytes(addr, struct.pack(SystemInfo.endian+"f", f))

    def writeDouble(self, addr, d):
        return self.writeBytes(addr, struct.pack(SystemInfo.endian+"d", d))

    def writeVoid(self, addr, p):
        return self.writeBytes(addr, struct.pack(SystemInfo.endian+"P", p))
