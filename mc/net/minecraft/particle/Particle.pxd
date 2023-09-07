# cython: language_level=3

from mc.cCompatibilityShims cimport Random
from mc.net.minecraft.renderer.Tesselator cimport Tesselator
from mc.net.minecraft.Entity cimport Entity

cdef class Particle(Entity):

    cdef:
        Random _random
        public int _tex
        public float _gravity
        public float _rCol
        public float _gCol
        public float _bCol
        public float _xd
        public float _yd
        public float _zd
        public float _uo
        public float _vo
        public float _size
        public int _lifetime
        public int _age

    cpdef tick(self)
