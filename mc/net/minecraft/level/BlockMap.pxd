# cython: language_level=3

cimport cython

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

    cdef list getEntities(self, oEntity, float x0, float y0, float z0,
                          float x1, float y1, float z1, list l)
    cpdef list getEntitiesWithinAABBExcludingEntity(self, entity, aabb)
    cpdef render(self, Frustum frustum, textures, float a)
