#!/usr/bin/env python
# encoding: utf-8

import sys

class SystemInfo(object):
    if sys.byteorder == "little":
        endian = "<"
    else:
        endian = ">"

class ProgPath(object):
    dot = "dot"
    display = "display"
    hexer = "hexer"
    hexedit = "hexedit"
    hexdump = "hexdmp"
    od = "od"

