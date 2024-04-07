# cython: language_level=3

cimport cython

from mc.net.minecraft.game.entity.Entity cimport Entity
from mc.net.minecraft.game.physics.AxisAlignedBB cimport AxisAlignedBB
from mc.net.minecraft.game.level.EntityMapSlot cimport EntityMapSlot

@cython.final
cdef class EntityMap:

    cdef:
        public int width
        public int depth
        public int height

        EntityMapSlot __slot0
        EntityMapSlot __slot1

        public list entityGrid
        public list all
        list __tmp

    cdef add(self, Entity entity)
    cdef remove(self, Entity entity)
    cdef list getEntities(self, Entity oEntity, float x0, float y0, float z0,
                          float x1, float y1, float z1)
    cdef list __addEntities(self, Entity oEntity, float x0, float y0, float z0,
                            float x1, float y1, float z1, list l)
    cpdef list getEntitiesWithinAABBExcludingEntity(self, Entity entity, AxisAlignedBB aabb)
    cdef updateEntities(self)
