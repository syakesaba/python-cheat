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

    @property
    def vsyscall(self):
        return self._findMap("[vsyscall]")

    @property
    def vdso(self):
        return self._findMap("[vdso]")

    def _findMap(self, pathname):
        for mp in self.maps:
            if mp.pathname == pathname:
                return mp

class SequentialMemoryDump(object):
    def __init__(self, start_address, end_address, dump_data):
        assert(type(start_address) == int)
        assert(type(end_address) == int)
        self.start_address = start_address
        self.end_address = end_address
        self.dump_data = dump_data

    def __lt__(self, other_memdump):
        assert(type(other_memdump) == type(self))
        pass

    def __le__(self, other_memdump):
        assert(type(other_memdump) == type(self))
        pass

    def __eq__(self, other_memdump):
        assert(type(other_memdump) == type(self))
        pass

    def __ne__(self, other_memdump):
        assert(type(other_memdump) == type(self))
        pass

    def __gt__(self, other_memdump):
        assert(type(other_memdump) == type(self))
        pass

    def __ge__(self, other_memdump):
        assert(type(other_memdump) == type(self))
        pass

    def __str__(self):
        return self.dump_data

    def __repr__(self):
        return "%s - %s %d bytes" % (hex(self.start_address), hex(self.end_address), len(self.dump_data))

    def bitmap(self):
        #BZdump
        pass

    def magic(self):
        #file command magic bytes detection
        pass
