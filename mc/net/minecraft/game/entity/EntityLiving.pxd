# cython: language_level=3

from mc.net.minecraft.game.entity.Entity cimport Entity
from mc.net.minecraft.game.entity.AILiving cimport AILiving

cdef class EntityLiving(Entity):

    cdef:
        public int heartsHalvesLife
        public float renderYawOffset
        public float prevRenderYawOffset
        float __prevRotationYawHead
        float __rotationYawHead
        int __maxAir
        public float _animStep
        public float _animStepO
        public int health
        public int prevHealth
        public int scoreValue
        public int air
        public int hurtTime
        public int maxHurtTime
        public float attackedAtYaw
        public int deathTime
        int __attackTime
        public float prevCameraPitch
        public float cameraPitch
        public AILiving entityAI

    cpdef onEntityUpdate(self)
    cpdef onLivingUpdate(self)
    cdef _fall(self, float d)
    cdef travel(self, float x, float z)
