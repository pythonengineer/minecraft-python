# cython: language_level=3

from mc.net.minecraft.Entity cimport Entity
from mc.net.minecraft.mob.ai.BasicAI cimport BasicAI

cdef class Mob(Entity):

    cdef:
        public int invulnerableDuration
        public float rot
        public float timeOffs
        public float speed
        public float rotA
        public float _yBodyRot
        public float _yBodyRotO
        public float _oRun
        public float _run
        public float _animStep
        public float _animStepO
        public int _tickCount
        public bint hasHair
        public str _textureName
        public bint allowAlpha
        public str modelName
        public float _bobStrength
        public int _deathScore
        public float rotOffs
        public int health
        public int lastHealth
        public int invulnerableTime
        public int airSupply
        public int hurtTime
        public int hurtDuration
        public float hurtDir
        public int deathTime
        public int attackTime
        public float oTilt
        public float tilt
        public bint _dead
        public BasicAI ai

    cpdef tick(self)
    cpdef aiStep(self)
    cpdef render(self, textures, float translation)
    cdef knockback(self, Entity entity, int hp, float xd, float zd)
    cdef _causeFallDamage(self, float d)
    cdef travel(self, float x, float z)
