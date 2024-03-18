# cython: language_level=3

cimport cython

from mc.net.minecraft.game.level.EntityMap cimport EntityMap

@cython.final
cdef class EntityMapSlot:

    cdef:
        public int xSlot
        public int ySlot
        public int zSlot
        EntityMap __entityMap

    cdef EntityMapSlot init(self, float x, float y, float z)
    cdef add(self, entity)
    cdef remove(self, entity)
