# -*- coding: utf-8 -*-

import pickle
import os

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

class MemoryDump(dict):
    def __init__(self,address_value=None):
        if address_value:
            dict.__init__(self, address_value)
        else:
            dict.__init__(self)

    def __hash__(self):
        return hash(pickle.dumps(self))

    def __hash__keys(self):
        return hash(pickle.dumps(self.keys()))

    def has_same_addresses(self, other_memdump):
        return self.__hash__keys() == other_memdump.__hash__keys()

    def has_same_addresses_values(self, other_memdump):
        return hash(self) == hash(other_memdump)

    def __lt__(self, other_memdump):
        assert(type(other_memdump) == type(self))
        assert(self.__hash__keys() == other_memdump.__hash__keys())
        return MemoryDump({k:self[k] for k in self if self[k] < other_memdump[k]})

    def __le__(self, other_memdump):
        assert(type(other_memdump) == type(self))
        assert(self.__hash__keys() == other_memdump.__hash__keys())
        return MemoryDump({k:self[k] for k in self if self[k] <= other_memdump[k]})

    def __eq__(self, other_memdump):
        assert(type(other_memdump) == type(self))
        assert(self.__hash__keys() == other_memdump.__hash__keys())
        return MemoryDump({k:self[k] for k in self if self[k] == other_memdump[k]})

    def __ne__(self, other_memdump):
        assert(type(other_memdump) == type(self))
        assert(self.__hash__keys() == other_memdump.__hash__keys())
        return MemoryDump({k:self[k] for k in self if self[k] != other_memdump[k]})

    def __gt__(self, other_memdump):
        assert(type(other_memdump) == type(self))
        assert(self.__hash__keys() == other_memdump.__hash__keys())
        return MemoryDump({k:self[k] for k in self if self[k] > other_memdump[k]})

    def __ge__(self, other_memdump):
        assert(type(other_memdump) == type(self))
        assert(self.__hash__keys() == other_memdump.__hash__keys())
        return MemoryDump({k:self[k] for k in self if self[k] >= other_memdump[k]})

    def __str__(self):
        #return os.linesep.join(["%016x : %016x %16s" % (k, self[k], "".join([ch for ch in self[k] if ord(ch) in range(0x20,0x7E)])) for k in self])
        return repr(self)

    def __repr__(self):
        return os.linesep.join(["%016x : %016x" % (k, self[k]) for k in self])

    def bitmap(self):
        #BZdump
        pass

    def magic(self):
        #file command magic bytes detection
        pass
