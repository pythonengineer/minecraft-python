# cython: language_level=3

from mc.net.minecraft.game.entity.EntityLiving cimport EntityLiving
from mc.net.minecraft.game.level.World cimport World
from mc.CompatibilityShims cimport Random

cdef class AILiving:

    cdef:
        Random __rand
        public float moveStrafing
        public float moveForward
        float __randomYawVelocity
        EntityLiving __entityLiving
        public bint isJumping
        int __fire
        float __moveSpeed
        int __entityAge

    cpdef onLivingUpdate(self, World world, EntityLiving mob)
    cpdef updatePlayerActionState(self)
