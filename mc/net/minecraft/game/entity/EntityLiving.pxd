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
        public str texture
        public int health
        public int prevHealth
        public int hurtTime
        public int maxHurtTime
        public float attackedAtYaw
        public int deathTime
        int __attackTime
        public float prevCameraPitch
        public float cameraPitch
        public AILiving _entityAI
        public float moveStrafing
        public float moveForward
        public float randomYawVelocity

    cpdef float _getEyeHeight(self)
    cdef _fall(self, float d)
    cdef travel(self, float x, float z)
