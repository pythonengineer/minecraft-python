# cython: language_level=3

from mc.net.minecraft.Entity cimport Entity
from mc.net.minecraft.mob.Mob cimport Mob
from mc.net.minecraft.level.Level cimport Level
from mc.cCompatibilityShims cimport Random

cdef class BasicAI:

    cdef:
        public int defaultLookAngle
        Random __rand
        public float xxa
        public float yya
        public float _yRotA
        public Level level
        public Mob mob
        public bint jumping
        public int _attackDelay
        public float runSpeed
        public int _noActionTime
        public Entity attackTarget

    cpdef tick(self, Level level, Mob mob)
    cpdef update(self)
