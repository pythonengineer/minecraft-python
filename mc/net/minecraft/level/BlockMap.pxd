# cython: language_level=3

cimport cython

from mc.net.minecraft.Entity cimport Entity
from mc.net.minecraft.phys.AABB cimport AABB
from mc.net.minecraft.level.Slot cimport Slot
from mc.net.minecraft.renderer.Frustum cimport Frustum

@cython.final
cdef class BlockMap:

    cdef:
        public Slot slot1
        public Slot slot2

        public list all
        public list tmp

        public int width
        public int depth
        public int height

        public list entityGrid

    cdef insert(self, Entity entity)
    cdef remove(self, Entity entity)
    cdef list getEntities(self, Entity oEntity, float x0, float y0, float z0,
                          float x1, float y1, float z1, list l)
    cdef list getEntitiesExcludingEntity(self, Entity entity, float x0, float y0,
                                         float z0, float x1, float y1, float z1)
    cpdef list getEntitiesWithinAABBExcludingEntity(self, Entity entity, AABB aabb)
    cdef list getEntitiesWithinAABBExcludingEntityList(self, Entity entity, AABB aabb, l)
    cdef clear(self)
    cdef tickAll(self)
    cpdef render(self, vec, Frustum frustum, textures, float a)
