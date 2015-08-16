# -*- coding: utf-8 -*-
from ptrace.debugger.process_error import ProcessError


class Register(object):
    def __init__(self, debugger):
        self.debugger = debugger

    def __getitem__(self, item):
        try:
            return self.debugger.target.getreg(item)
        except ProcessError as e:
            pass
