# cython: language_level=3

cimport cython

cpdef unsigned long long getMillis()

cdef class Random:

    cdef float randFloatM(self, float multiply)
    cdef float randFloat(self)
    cdef int nextInt(self, int limit)

cdef class Bits:

    cdef long makeLong(self, unsigned char b7, unsigned char b6, unsigned char b5,
                       unsigned char b4, unsigned char b3, unsigned char b2,
                       unsigned char b1, unsigned char b0)
    cdef int makeInt(self, unsigned char b3, unsigned char b2,
                     unsigned char b1, unsigned char b0)
    cdef short makeShort(self, unsigned char b1, unsigned char b0)

cpdef enum ByteOrder:
    BIG_ENDIAN = 0
    LITTLE_ENDIAN = 1

cdef class Buffer(Bits):

    cdef:
        int _position
        int _limit
        int _capacity
        bint _order

    cpdef long getLong(self)
    cpdef int getInt(self)
    cpdef short getShort(self)
    cpdef double getDouble(self)
    cpdef float getFloat(self)

    cpdef order(self, bint order)
    cpdef flip(self)
    cpdef limit(self, int limit)
    cpdef position(self, int position=?)
    cpdef remaining(self)

    cpdef clear(self)
    cpdef capacity(self)
    cpdef compact(self)

    cdef int __nextIndex(self, int nb=?)
    cdef int nextGetIndex(self, int nb=?)
    cdef int nextPutIndex(self, int nb=?)

    cdef int checkIndex(self, int i)
    cdef bint checkBounds(self, int off, int length, int size)

@cython.final
cdef class ByteBuffer(Buffer):
    cdef:
        unsigned char[:] __array
        object __dataPtr

    cpdef inline put(self, unsigned char value)
    cpdef inline unsigned char get(self)
    cpdef inline unsigned char getAt(self, int idx)
    cdef inline __getDataPtr(self)

@cython.final
cdef class IntBuffer(Buffer):
    cdef:
        int[:] __array
        object __dataPtr

    cpdef inline put(self, int value)
    cpdef inline int get(self)
    cpdef inline int getAt(self, int idx)
    cdef inline __getDataPtr(self)

@cython.final
cdef class FloatBuffer(Buffer):
    cdef:
        float[:] __array
        object __dataPtr

    cpdef inline put(self, float value)
    cdef putFloats(self, float* src, int offset, int length)
    cpdef inline float get(self)
    cpdef inline float getAt(self, int idx)
    cdef getFloats(self, float*, int size)
    cdef inline __getDataPtr(self)
