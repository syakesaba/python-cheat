# -*- coding: utf-8 -*-


class Memory(object):
    def __init__(self, debugger):
        self.debugger = debugger
        self._mapping = None
  
    @property
    def maps(self):
        self._mapping = self.debugger.target.readMappings()
        return self._mapping

    @property
    def heap(self):
        return self._findMap("[heap]")

    @property
    def stack(self):
        return self._findMap("[stack]")

    def _findMap(self, pathname):
        for mp in self.maps:
            if mp.pathname == pathname:
                return mp
