class CheatMemory(object):    
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

if __name__ == "__main__":
    from __init__ import CheaterDebugger
    pid = int(raw_input("input pid: "))
    d = CheaterDebugger()
    p = d.addProcess(pid, False, None)
    p.memory = CheatMemory(p)
    p.cont()
    print p.memory.heap
    print p.memory.stack