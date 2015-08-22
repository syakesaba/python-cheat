# -*- coding: utf-8 -*-

import ptrace.debugger
import struct
import signal

from config import SystemInfo, ProgramPath
from memory import Memory
from register import Register
from functools import wraps
from ptrace.debugger.process_error import ProcessError, PtraceError


class Debugger(ptrace.debugger.PtraceDebugger):
    def __init__(self):
        ptrace.debugger.PtraceDebugger.__init__(self)
        self._target_process = None

    @classmethod
    def lock_it(cls, f):
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

    @property
    def memory(self):
        return Memory(self)

    @memory.setter
    def memory(self, mem):
        raise Exception("Restore Memory is not impletemted")

    def addProcess(self, pid, is_attached, parent=None):
        ret = ptrace.debugger.PtraceDebugger.addProcess(self, pid, is_attached, parent)
        if ret is not None and self.target is None:
            self.target = ret
            self.start_target()
        return ret

    def deleteProcess(self, process=None, pid=None):
        ret = ptrace.debugger.PtraceDebugger.deleteProcess(self, process, pid)
        if self.target is not None:
            if process is not None and self.target.pid == process.pid or \
                    pid is not None and self.target.pid == pid:
                if self.list:
                    self.target = self.list[0]
                else:
                    self.target = None
        return ret

    def switch_target(self, target_pid):
        self.target = self[self.target_pid]

    def start_target(self):
        return self.target.cont()
        # return self.target.kill(signal.SIGCONT)

    def stop_target(self):
        return self.target.kill(signal.SIGSTOP)

    def show_target(self):
        print self.target

# ============ Searching Memory

    def searchBytes(self, s):
        matchings = set()
#        try:
#            self.target.getInstrPointer()
#        except ProcessError:
#            self.stop_target()
#        except PtraceError:
#            self.stop_target()
        for mappings in self.target.readMappings():
            if mappings.pathname in ["[vsyscall]","[vdso]"]:
                #Fake-bin
                continue
            print "Searching " + str(mappings)
            try:
                for matching in mappings.search(s):
                    print "matched => " + str(hex(matching))
                    matchings.add(matching)
            except Exception as e:
                print "Unknown Error: ",e
        # self.start_target()
        return matchings

    def searchString(self, s, encoding=None):
        #TODO string to binary
        return self.searchBytes(s)

    def searchBool(self, b):
        return self.searchBytes(struct.pack(SystemInfo.endian + "?", b))

    def searchShort(self, s):
        return self.searchBytes(struct.pack(SystemInfo.endian + "h", s))

    def searchShortUnsigned(self, s):
        return self.searchBytes(struct.pack(SystemInfo.endian + "H", s))

    def searchInt(self, i):
        return self.searchBytes(struct.pack(SystemInfo.endian + "i", i))

    def searchIntUnsigned(self, i):
        return self.searchBytes(struct.pack(SystemInfo.endian + "I", i))

    def searchLong(self, l):
        return self.searchBytes(struct.pack(SystemInfo.endian + "l", l))

    def searchLongUnsigned(self, l):
        return self.searchBytes(struct.pack(SystemInfo.endian + "L", l))

    def searchLongLong(self, ll):
        return self.searchBytes(struct.pack(SystemInfo.endian + "q", ll))

    def searchLongLongUnsigned(self, ll):
        return self.searchBytes(struct.pack(SystemInfo.endian + "Q", ll))

    def searchFloat(self, f):
        return self.searchBytes(struct.pack(SystemInfo.endian + "f", f))

    def searchDouble(self, d):
        return self.searchBytes(struct.pack(SystemInfo.endian + "d", d))

    def searchVoid(self, p):
        return self.searchBytes(struct.pack(SystemInfo.endian + "P", p))

# Dumping-Searching
# less than, greater than, equal, diff
    def dumpAllMemory(self):
        pass
    def diffMemory(self):
        pass
# or implement in different file?

# Pythonic Searcing
    def searchMatcher(self, bytes_per_read, function):
        pass

# Pointer Searching
    def serachPointer(self):
        pass

# ============ Reading Memory

    def readBytes(self, addr, length):
        if not self.target.is_attached:
            self.addProcess(self.target.pid, False)
        ret = self.target.readBytes(addr, length)
        return ret

    def readString(self, addr, length, encoding=None):
        #TODO string to binary
        return self.readBytes(addr, length)

    def readBool(self, addr):
        return struct.unpack(SystemInfo.endian + "?", self.readBytes(addr, SystemInfo.sizeof.bool))

    def readShort(self, addr):
        return struct.unpack(SystemInfo.endian + "h", self.readBytes(addr, SystemInfo.sizeof.short))

    def readShortUnsigned(self, addr):
        return struct.unpack(SystemInfo.endian + "H", self.readBytes(addr, SystemInfo.sizeof.ushort))

    def readInt(self, addr):
        return struct.unpack(SystemInfo.endian + "i", self.readBytes(addr, SystemInfo.sizeof.int))

    def readIntUnsigned(self, addr):
        return struct.unpack(SystemInfo.endian + "I", self.readBytes(addr, SystemInfo.sizeof.uint))

    def readLong(self, addr):
        return struct.unpack(SystemInfo.endian + "l", self.readBytes(addr, SystemInfo.sizeof.long))

    def readLongUnsigned(self, addr):
        return struct.unpack(SystemInfo.endian + "L", self.readBytes(addr, SystemInfo.sizeof.ulong))

    def readLongLong(self, addr):
        return struct.unpack(SystemInfo.endian + "q", self.readBytes(addr, SystemInfo.sizeof.longlong))

    def readLongLongUnsigned(self, addr):
        return struct.unpack(SystemInfo.endian + "Q", self.readBytes(addr, SystemInfo.sizeof.ulonglong))

    def readFloat(self, addr):
        return struct.unpack(SystemInfo.endian + "f", self.readBytes(addr, SystemInfo.sizeof.float))

    def readDouble(self, addr):
        return struct.unpack(SystemInfo.endian + "d", self.readBytes(addr, SystemInfo.sizeof.double))

    def readVoid(self, addr):
        return struct.unpack(SystemInfo.endian + "P", self.readBytes(addr, SystemInfo.sizeof.void))

# ============ Writing Memory

    def writeBytes(self, addr, data):
        if not self.target.is_stopped:
            self.stop_target()
        ret = self.target.writeBytes(addr, data)
        # iself.start_target()
        return ret

    def writeString(self, addr, length, encoding=None):
        #TODO string to binary
        return self.writeBytes(addr, length)

    def writeBool(self, addr, b):
        return self.writeBytes(addr, struct.pack(SystemInfo.endian + "?", b))

    def writeShort(self, addr, s):
        return self.writeBytes(addr, struct.pack(SystemInfo.endian + "h", s))

    def writeShortUnsigned(self, addr, s):
        return self.writeBytes(addr, struct.pack(SystemInfo.endian + "H", s))

    def writeInt(self, addr, i):
        return self.writeBytes(addr, struct.pack(SystemInfo.endian + "i", i))

    def writeIntUnsigned(self, addr, i):
        return self.writeBytes(addr, struct.pack(SystemInfo.endian + "I", i))

    def writeLong(self, addr, l):
        return self.writeBytes(addr, struct.pack(SystemInfo.endian + "l", l))

    def writeLongUnsigned(self, addr, l):
        return self.writeBytes(addr, struct.pack(SystemInfo.endian + "L", l))

    def writeLongLong(self, addr, ll):
        return self.writeBytes(addr, struct.pack(SystemInfo.endian + "q", ll))

    def writeLongLongUnsigned(self, addr, ll):
        return self.writeBytes(addr, struct.pack(SystemInfo.endian + "Q", ll))

    def writeFloat(self, addr, f):
        return self.writeBytes(addr, struct.pack(SystemInfo.endian + "f", f))

    def writeDouble(self, addr, d):
        return self.writeBytes(addr, struct.pack(SystemInfo.endian + "d", d))

    def writeVoid(self, addr, p):
        return self.writeBytes(addr, struct.pack(SystemInfo.endian + "P", p))
