# cython: language_level=3

cdef class TextureFX:

    cdef:
        public int iconIndex
        public list imageData

    cpdef onTick(self)
