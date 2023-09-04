# cython: language_level=3

cimport cython

from mc.net.minecraft.level.BlockMap cimport BlockMap

@cython.final
cdef class Slot:

    cdef:
        public int xSlot
        public int ySlot
        public int zSlot
        BlockMap __blockInMapArray

    cdef Slot init(self, float x, float y, float z)
    cdef add(self, entity)
    cdef remove(self, entity)
