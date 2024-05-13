# cython: language_level=3

from mc.net.minecraft.client.render.Tessellator cimport Tessellator
from mc.net.minecraft.game.entity.Entity cimport Entity

cdef class EntityFX(Entity):

    cdef:
        public int _particleTextureIndex
        public float _particleGravity
        public float _particleRed
        public float _particleGreen
        public float _particleBlue
        public float _motionX1
        public float _motionY1
        public float _motionZ1
        public float _particleTextureJitterX
        public float _particleTextureJitterY
        public float _particleScale
        public int _particleMaxAge
        public int _particleAge
