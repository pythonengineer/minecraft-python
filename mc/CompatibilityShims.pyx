# cython: language_level=3
# cython: cdivision=True, boundscheck=False, wraparound=False, nonecheck=False

cimport cython

from libc.string cimport memcpy
from libc.stdlib cimport srand, rand, RAND_MAX
from libc.time cimport time

from pyglet import gl

import ctypes
import time as pytime

import numpy as np
cimport numpy as np

cpdef unsigned long long getMillis():
    return <unsigned long long>(pytime.time() * 1000)

cdef bint Random_seeded = False

cdef class Random:

    property seeded:

        def __get__(self):
            return Random_seeded

        def __set__(self, x):
            global Random_seeded
            Random_seeded = x

    def __init__(self, seed=0):
        if not self.seeded:
            if seed == 0:
                srand(time(NULL))
            else:
                srand(seed)

            self.seeded = True

    cdef float randFloatM(self, float multiply):
        return self.randFloat() * multiply

    cdef float randFloat(self):
        return rand() / <float>RAND_MAX

    cdef int nextInt(self, int limit):
        cdef double scaleFactor
        cdef int value

        if limit <= 0:
            raise ValueError('limit must be a positive integer')

        scaleFactor = limit / (RAND_MAX + 1.0)
        value = <int>(rand() * scaleFactor)

        return value

cdef class Bits:

    cdef long makeLong(self, unsigned char b7, unsigned char b6, unsigned char b5,
                       unsigned char b4, unsigned char b3, unsigned char b2,
                       unsigned char b1, unsigned char b0):
        return ((b7       ) << 56) | \
               ((b6 & 0xFF) << 48) | \
               ((b5 & 0xFF) << 40) | \
               ((b4 & 0xFF) << 32) | \
               ((b3 & 0xFF) << 24) | \
               ((b2 & 0xFF) << 16) | \
               ((b1 & 0xFF) <<  8) | \
               ((b0 & 0xFF)      )

    cdef int makeInt(self, unsigned char b3, unsigned char b2,
                     unsigned char b1, unsigned char b0):
        return ((b3       ) << 24) | \
               ((b2 & 0xFF) << 16) | \
               ((b1 & 0xFF) <<  8) | \
               ((b0 & 0xFF)      )

    cdef short makeShort(self, unsigned char b1, unsigned char b0):
        return (b1 << 8) | (b0 & 0xFF)

cdef class Buffer(Bits):

    def __init__(self, capacity):
        self._position = 0
        self._limit = 0
        self._capacity = capacity
        self._order = ByteOrder.BIG_ENDIAN

    def __len__(self):
        return self._capacity

    def putBytes(self, src):
        return self.putOffset(src, 0, len(src))

    def putOffset(self, src, int offset, int length):
        cdef int rem, i, n

        assert self.checkBounds(offset, length, len(src))
        assert self._position <= self._limit
        rem = self._limit - self._position if self._position <= self._limit else 0
        if length > rem:
            raise Exception

        for i, n in enumerate(range(offset, offset + length)):
            self[self._position + n] = src[i]

        self._position += length

        return self

    cpdef long getLong(self):
        cdef int pos = self.nextGetIndex(1 << 3)
        if self._order == ByteOrder.BIG_ENDIAN:
            return self.makeLong(self[pos    ], self[pos + 1],
                                 self[pos + 2], self[pos + 3],
                                 self[pos + 4], self[pos + 5],
                                 self[pos + 6], self[pos + 7])
        elif self._order == ByteOrder.LITTLE_ENDIAN:
            return self.makeLong(self[pos + 7], self[pos + 6],
                                 self[pos + 5], self[pos + 4],
                                 self[pos + 3], self[pos + 2],
                                 self[pos + 1], self[pos    ])

    cpdef int getInt(self):
        cdef int pos = self.nextGetIndex(1 << 2)
        if self._order == ByteOrder.BIG_ENDIAN:
            return self.makeInt(self[pos    ], self[pos + 1],
                                self[pos + 2], self[pos + 3])
        elif self._order == ByteOrder.LITTLE_ENDIAN:
            return self.makeInt(self[pos + 3], self[pos + 2],
                                self[pos + 1], self[pos    ])

    cpdef short getShort(self):
        cdef int pos = self.nextGetIndex(1 << 1)
        if self._order == ByteOrder.BIG_ENDIAN:
            return self.makeShort(self[pos    ], self[pos + 1])
        elif self._order == ByteOrder.LITTLE_ENDIAN:
            return self.makeShort(self[pos + 1], self[pos    ])

    cpdef double getDouble(self):
        cdef long value
        cdef double dValue
        cdef double* dptr
        cdef int pos = self.nextGetIndex(1 << 3)
        if self._order == ByteOrder.BIG_ENDIAN:
            value = self.makeLong(self[pos    ], self[pos + 1],
                                  self[pos + 2], self[pos + 3],
                                  self[pos + 4], self[pos + 5],
                                  self[pos + 6], self[pos + 7])
        elif self._order == ByteOrder.LITTLE_ENDIAN:
            value = self.makeLong(self[pos + 7], self[pos + 6],
                                  self[pos + 5], self[pos + 4],
                                  self[pos + 3], self[pos + 2],
                                  self[pos + 1], self[pos    ])

        dptr = <double*>&value
        dValue = dptr[0]
        return dValue

    cpdef float getFloat(self):
        cdef int pos, value
        cdef float fValue
        cdef float* fptr

        pos = self.nextGetIndex(1 << 2)
        if self._order == ByteOrder.BIG_ENDIAN:
            value = self.makeInt(self[pos    ], self[pos + 1],
                                 self[pos + 2], self[pos + 3])
        elif self._order == ByteOrder.LITTLE_ENDIAN:
            value = self.makeInt(self[pos + 3], self[pos + 2],
                                 self[pos + 1], self[pos    ])

        fptr = <float*>&value
        fValue = fptr[0]
        return fValue

    cpdef order(self, bint order):
        self._order = order

    cpdef flip(self):
        self._limit = self._position
        self._position = 0
        return self

    cpdef limit(self, int limit):
        if limit < 0 or limit > self._capacity:
            return self

        self._limit = limit
        if self._position > limit:
            self._position = limit

        return self

    cpdef position(self, int position=-1):
        if position == -1:
            return self._position
        if position < 0 or position >= self._capacity:
            raise Exception
        if position > self._limit:
            raise Exception

        self._position = position
        return self

    cpdef remaining(self):
        return self._limit - self._position

    cpdef clear(self):
        self._position = 0
        self._limit = self._capacity
        return self

    cpdef capacity(self):
        return self._capacity

    cpdef compact(self):
        assert self._position <= self._limit

        rem = self._limit - self._position if self._position <= self._limit else 0
        self[:rem] = self[self._position:self._position + rem]

        self._position = rem
        self._limit = self._capacity

        return self

    cdef int __nextIndex(self, int nb=-1):
        if nb != -1:
            if self._limit - self._position < nb:
                raise Exception
        elif self._position >= self._limit:
            raise Exception

        if nb == -1:
            nb = 1

        p = self._position
        self._position += nb
        return p

    cdef int nextGetIndex(self, int nb=-1): return self.__nextIndex(nb)
    cdef int nextPutIndex(self, int nb=-1): return self.__nextIndex(nb)

    cdef int checkIndex(self, int i):
        if i < 0 or i >= self._limit:
            raise Exception

        return i

    cdef bint checkBounds(self, int off, int length, int size):
        if (off | length | (off + length) | (size - (off + length))) < 0:
            raise Exception

        return True

cdef class ByteBuffer(Buffer):

    def __init__(self, capacity):
        Buffer.__init__(self, capacity)
        self.__array = np.zeros(capacity, dtype=np.ubyte)

    def __setitem__(self, key, value):
        cdef int i, k, idx
        if isinstance(key, slice):
            indices = range(*key.indices(self._capacity))
            if len(indices) != len(value):
                raise ValueError('Slice assignment size does not match value size')

            for i, idx in enumerate(indices):
                self.__array[idx] = value[i]
        elif isinstance(key, int):
            k = key
            if k < 0 or k >= self._capacity:
                raise IndexError

            self.__array[k] = <unsigned char>(value & 0xFF)

    def __getitem__(self, key):
        cdef int i, k
        if isinstance(key, slice):
            return [self.__array[i] for i in range(*key.indices(self._capacity))]
        elif isinstance(key, int):
            k = key
            if k < 0 or k >= self._capacity:
                raise IndexError

            return self.__array[k]

    cpdef inline put(self, unsigned char value):
        self[self.nextPutIndex()] = value
        return self

    cpdef inline unsigned char get(self):
        return self[self.nextGetIndex()]

    cpdef inline unsigned char getAt(self, int idx):
        return self[self.checkIndex(idx)]

    def getBytes(self, b):
        cdef int rem

        assert self.checkBounds(0, len(b), len(b))
        assert self._position <= self._limit
        rem = self._limit - self._position if self._position <= self._limit else 0
        if len(b) > rem:
            raise Exception

        sliced = self[self._position:self._position + len(b)]
        b[:] = [<unsigned char>e for e in sliced]

        self._position += len(b)
        return self

    cdef inline __getDataPtr(self):
        if not self.__dataPtr:
            self.__dataPtr = np.asarray(self.__array).ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte))

        return self.__dataPtr

    def glTexImage2D(self, int target, int level, int internalformat,
                     int width, int height, int border, int format,
                     int type):
        gl.glTexImage2D(target, level, internalformat, width, height,
                        border, format, type, self.__getDataPtr())

    def glTexSubImage2D(self, int target, int level, int xoffset, int yoffset,
                        int width, int height, int format, int type):
        gl.glTexSubImage2D(target, level, xoffset, yoffset, width, height,
                           format, type, self.__getDataPtr())

    def glReadPixels(self, int x, int y, int width, int height, int format, int type):
        gl.glReadPixels(x, y, width, height, format, type, self.__getDataPtr())

cdef class IntBuffer(Buffer):

    def __init__(self, capacity):
        Buffer.__init__(self, capacity)
        self.__array = np.zeros(capacity, dtype=np.int32)

    def __setitem__(self, key, value):
        cdef int i, k, idx
        if isinstance(key, slice):
            indices = range(*key.indices(self._capacity))
            if len(indices) != len(value):
                raise ValueError('Slice assignment size does not match value size')

            for i, idx in enumerate(indices):
                self.__array[idx] = value[i]
        elif isinstance(key, int):
            k = key
            if k < 0 or k >= self._capacity:
                raise IndexError

            self.__array[k] = value

    def __getitem__(self, key):
        cdef int i, k
        if isinstance(key, slice):
            return [self.__array[i] for i in range(*key.indices(self._capacity))]
        elif isinstance(key, int):
            k = key
            if k < 0 or k >= self._capacity:
                raise IndexError

            return self.__array[k]

    cpdef inline put(self, int value):
        self[self.nextPutIndex()] = value
        return self

    cpdef inline int get(self):
        return self[self.nextGetIndex()]

    cpdef inline int getAt(self, int idx):
        return self[self.checkIndex(idx)]

    cdef inline __getDataPtr(self):
        if not self.__dataPtr:
            self.__dataPtr = np.asarray(self.__array).ctypes.data_as(ctypes.POINTER(ctypes.c_int))

        return self.__dataPtr

    def glCallLists(self, int n, int type):
        gl.glCallLists(n, type, self.__getDataPtr())

    def glDrawElements(self, int mode, int count, int type):
        gl.glDrawElements(mode, count, type, self.__getDataPtr())

cdef class FloatBuffer(Buffer):

    def __init__(self, capacity):
        Buffer.__init__(self, capacity)
        self.__array = np.zeros(capacity, dtype=np.float32)

    def __setitem__(self, key, value):
        cdef int i, k, idx
        if isinstance(key, slice):
            indices = range(*key.indices(self._capacity))
            if len(indices) != len(value):
                raise ValueError('Slice assignment size does not match value size')

            for i, idx in enumerate(indices):
                self.__array[idx] = value[i]
        elif isinstance(key, int):
            k = key
            if k < 0 or k >= self._capacity:
                raise IndexError

            self.__array[k] = value

    def __getitem__(self, key):
        cdef int i, k
        if isinstance(key, slice):
            return [self.__array[i] for i in range(*key.indices(self._capacity))]
        elif isinstance(key, int):
            k = key
            if k < 0 or k >= self._capacity:
                raise IndexError

            return self.__array[k]

    cpdef inline put(self, float value):
        self[self.nextPutIndex()] = value
        return self

    cdef putFloats(self, float* src, int offset, int length):
        cdef int i, rem

        assert self.checkBounds(offset, length, length)
        assert self._position <= self._limit
        rem = self._limit - self._position if self._position <= self._limit else 0
        if length > rem:
            raise Exception

        cdef float[:] dest = self.__array[self._position + offset:self._position + offset + length]
        for i in range(length):
            dest[i] = src[i]

        self._position += length

        return self

    cpdef inline float get(self):
        return self[self.nextGetIndex()]

    cpdef inline float getAt(self, int idx):
        return self[self.checkIndex(idx)]

    def getBytes(self, b):
        cdef int rem

        assert self.checkBounds(0, len(b), len(b))
        assert self._position <= self._limit
        rem = self._limit - self._position if self._position <= self._limit else 0
        if len(b) > rem:
            raise Exception

        sliced = self[self._position:self._position + len(b)]
        b[:] = [<float>e for e in sliced]

        self._position += len(b)
        return self

    cdef getFloats(self, float* array, int size):
        cdef int rem, i

        assert self.checkBounds(0, size, size)
        assert self._position <= self._limit
        rem = self._limit - self._position if self._position <= self._limit else 0
        if size > rem:
            raise Exception

        cdef float* src = &self.__array[self._position]
        memcpy(array, src, size * sizeof(float))

        self._position += size
        return self

    cdef inline __getDataPtr(self):
        if not self.__dataPtr:
            self.__dataPtr = np.asarray(self.__array).ctypes.data_as(ctypes.POINTER(ctypes.c_float))

        return self.__dataPtr

    def glFogfv(self, int pname):
        gl.glFogfv(pname, self.__getDataPtr())

    def glLightfv(self, int light, int pname):
        gl.glLightfv(light, pname, self.__getDataPtr())

    def glLightModelfv(self, int pname):
        gl.glLightModelfv(pname, self.__getDataPtr())

    def glVertexPointer(self, int size, int type, int stride):
        gl.glVertexPointer(size, type, stride, self.__getDataPtr())

    def glNormalPointer(self, int type, int stride):
        gl.glNormalPointer(type, stride, self.__getDataPtr())

    def glTexCoordPointer(self, int size, int type, int stride):
        gl.glTexCoordPointer(size, type, stride, self.__getDataPtr())

    def glInterleavedArrays(self, int format, int stride):
        gl.glInterleavedArrays(format, stride, self.__getDataPtr())

    def glMultMatrix(self):
        gl.glMultMatrixf(self.__getDataPtr())

cdef class BufferUtils:

    def wrapByteBuffer(byteArray):
        return ByteBuffer(len(byteArray)).clear().putBytes(byteArray).clear()

    def createByteBuffer(capacity):
        return ByteBuffer(capacity).clear()

    def createIntBuffer(capacity):
        return IntBuffer(capacity).clear()

    def createFloatBuffer(capacity):
        return FloatBuffer(capacity).clear()
