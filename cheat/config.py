#!/usr/bin/env python
# encoding: utf-8

import sys
import struct


class Config(object):
    """
    The ConfigClass from scapy!
    """
    def configure(self, cnf):
        self.__dict__ = cnf.__dict__.copy()

    def __repr__(self):
        return str(self)

    def __str__(self):
        s = ""
        keys = self.__class__.__dict__.copy()
        keys.update(self.__dict__)
        keys = keys.keys()
        keys.sort()
        for i in keys:
            if i[0] != "_":
                r = repr(getattr(self, i))
                r = " ".join(r.split())
                wlen = 76 - max(len(i), 10)
                if len(r) > wlen:
                    r = r[:wlen-3] + "..."
                s += "%-10s = %s\n" % (i, r)
        return s[:-1]


class Sizeof(Config):
    bool = struct.calcsize("b")
    short = struct.calcsize("h")
    ushort = struct.calcsize("H")
    int = struct.calcsize("i")
    uint = struct.calcsize("I")
    long = struct.calcsize("l")
    ulong = struct.calcsize("L")
    longlong = struct.calcsize("q")
    ulonglong = struct.calcsize("Q")
    float = struct.calcsize("f")
    double = struct.calcsize("d")
    void = struct.calcsize("P")


class ProgramPath(Config):
    dot = "dot"
    display = "display"
    hexer = "hexer"
    hexedit = "hexedit"
    hexdump = "hexdmp"
    od = "od"


class SystemInfo(Config):
    if sys.byteorder == "little":
        endian = "<"
    else:
        endian = ">"
    sizeof = Sizeof()
