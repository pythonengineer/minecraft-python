# cython: language_level=3

cimport cython

from mc.net.minecraft.game.entity.Entity cimport Entity
from mc.net.minecraft.game.physics.AxisAlignedBB cimport AxisAlignedBB
from mc.net.minecraft.game.level.EntityMapSlot cimport EntityMapSlot
from mc.net.minecraft.client.render.ClippingHelper cimport ClippingHelper

@cython.final
cdef class EntityMap:

    cdef:
        public int xSlot
        public int ySlot
        public int zSlot

        public EntityMapSlot slot0
        public EntityMapSlot slot1

        public list entityGrid
        public list entities
        list __entitiesExcludingEntity

    cpdef list getEntitiesWithinAABBExcludingEntity(self, Entity entity, AxisAlignedBB aabb)
    cdef tickAll(self)
    cpdef render(self, vec, ClippingHelper frustum, renderManager, renderEngine, float a)
