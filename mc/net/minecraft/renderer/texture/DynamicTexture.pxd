# cython: language_level=3

cdef class DynamicTexture:

    cdef:
        public int tex
        public list pixels
        public bint anaglyph

    cpdef tick(self)
