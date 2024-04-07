# cython: language_level=3

from mc.net.minecraft.game.entity.Entity cimport Entity
from mc.net.minecraft.game.entity.EntityLiving cimport EntityLiving
from mc.net.minecraft.game.level.World cimport World
from mc.CompatibilityShims cimport Random

cdef class AILiving:

    cdef:
        Random __rand
        public float _moveStrafing
        public float _moveForward
        float __randomYawVelocity
        EntityLiving __targetToAttack
        public bint _isJumping
        int __fire
        float __moveSpeed
        int __entityAge
        Entity __playerToAttack

    cpdef onLivingUpdate(self, World world, EntityLiving mob)
    cpdef updatePlayerActionState(self)
