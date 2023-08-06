# cython: language_level=3

from pyglet import gl

cdef class Tesselator:
    MAX_FLOATS = 524288

    def __cinit__(self):
        self.max_floats = self.MAX_FLOATS
        self.__buffer = (gl.GLfloat * self.MAX_FLOATS)()
        self.len = 3

        self.u = 0.0
        self.v = 0.0
        self.r = 0.0
        self.g = 0.0
        self.b = 0.0

        self.hasColor = False
        self.hasTexture = False

    cpdef flush(self):
        cdef int rem, i, n

        self.__buffer._position = 0
        self.__buffer._limit = len(self.__buffer)

        rem = self.__buffer._limit - self.__buffer._position if self.__buffer._position <= self.__buffer._limit else 0
        if self.p > rem:
            raise Exception

        for i, n in enumerate(range(self.p)):
            self.__buffer[self.__buffer._position + n] = self.__array[i]

        self.__buffer._position += self.p
        self.__buffer._limit = self.__buffer._position
        self.__buffer._position = 0

        if self.hasTexture and self.hasColor:
            gl.glInterleavedArrays(gl.GL_T2F_C3F_V3F, 0, self.__buffer)
        elif self.hasTexture:
            gl.glInterleavedArrays(gl.GL_T2F_V3F, 0, self.__buffer)
        elif self.hasColor:
            gl.glInterleavedArrays(gl.GL_C3F_V3F, 0, self.__buffer)
        else:
            gl.glInterleavedArrays(gl.GL_V3F, 0, self.__buffer)

        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        if self.hasTexture:
            gl.glEnableClientState(gl.GL_TEXTURE_COORD_ARRAY)
        if self.hasColor:
            gl.glEnableClientState(gl.GL_COLOR_ARRAY)

        gl.glDrawArrays(gl.GL_QUADS, 0, self.vertices)

        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)
        if self.hasTexture:
            gl.glDisableClientState(gl.GL_TEXTURE_COORD_ARRAY)
        if self.hasColor:
            gl.glDisableClientState(gl.GL_COLOR_ARRAY)

        self.clear()

    cdef clear(self):
        self.vertices = 0
        self.__buffer._position = 0
        self.__buffer._limit = len(self.__buffer)
        self.p = 0

    cpdef init(self):
        self.clear()
        self.hasColor = False
        self.hasTexture = False

    cpdef tex(self, float u, float v):
        if not self.hasTexture:
            self.len += 2

        self.hasTexture = True
        self.u = u
        self.v = v

    cpdef color(self, float r, float g, float b):
        if not self.hasColor:
            self.len += 3

        self.hasColor = True
        self.r = r
        self.g = g
        self.b = b

    cpdef vertexUV(self, float x, float y, float z, float u, float v):
        self.tex(u, v)
        self.vertex(x, y, z)

    cpdef vertex(self, float x, float y, float z):
        if self.hasTexture:
            self.__array[self.p] = self.u
            self.p += 1
            self.__array[self.p] = self.v
            self.p += 1
        if self.hasColor:
            self.__array[self.p] = self.r
            self.p += 1
            self.__array[self.p] = self.g
            self.p += 1
            self.__array[self.p] = self.b
            self.p += 1
        self.__array[self.p] = x
        self.p += 1
        self.__array[self.p] = y
        self.p += 1
        self.__array[self.p] = z
        self.p += 1

        self.vertices += 1
        if self.vertices % 4 == 0 and (self.p >= self.max_floats - self.len * 4):
            self.flush()

tesselator = Tesselator()
