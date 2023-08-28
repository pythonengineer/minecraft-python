# cython: language_level=3

from pyglet import gl

cdef class Tesselator:
    MAX_FLOATS = 524288

    def __cinit__(self):
        self.max_floats = self.MAX_FLOATS
        self.__buffer = (gl.GLfloat * self.MAX_FLOATS)()
        self.__len = 3

    cpdef void end(self):
        cdef int rem, i, n

        if self.__vertices > 0:
            self.__buffer._position = 0
            self.__buffer._limit = len(self.__buffer)

            rem = self.__buffer._limit - self.__buffer._position if self.__buffer._position <= self.__buffer._limit else 0
            if self.__p > rem:
                raise Exception

            for i, n in enumerate(range(self.__p)):
                self.__buffer[self.__buffer._position + n] = self.__array[i]

            self.__buffer._position += self.__p
            self.__buffer._limit = self.__buffer._position
            self.__buffer._position = 0

            if self.__hasTexture and self.__hasColor:
                gl.glInterleavedArrays(gl.GL_T2F_C3F_V3F, 0, self.__buffer)
            elif self.__hasTexture:
                gl.glInterleavedArrays(gl.GL_T2F_V3F, 0, self.__buffer)
            elif self.__hasColor:
                gl.glInterleavedArrays(gl.GL_C3F_V3F, 0, self.__buffer)
            else:
                gl.glInterleavedArrays(gl.GL_V3F, 0, self.__buffer)

            gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
            if self.__hasTexture:
                gl.glEnableClientState(gl.GL_TEXTURE_COORD_ARRAY)
            if self.__hasColor:
                gl.glEnableClientState(gl.GL_COLOR_ARRAY)

            gl.glDrawArrays(gl.GL_QUADS, gl.GL_POINTS, self.__vertices)

            gl.glDisableClientState(gl.GL_VERTEX_ARRAY)
            if self.__hasTexture:
                gl.glDisableClientState(gl.GL_TEXTURE_COORD_ARRAY)
            if self.__hasColor:
                gl.glDisableClientState(gl.GL_COLOR_ARRAY)

        self.__clear()

    cdef void __clear(self):
        self.__vertices = 0
        self.__buffer._position = 0
        self.__buffer._limit = len(self.__buffer)
        self.__p = 0

    cpdef void begin(self):
        self.__clear()
        self.__hasColor = False
        self.__hasTexture = False
        self.__noColor = False

    cpdef void colorFloat(self, float r, float g, float b):
        if self.__noColor:
            return

        if not self.__hasColor:
            self.__len += 3

        self.__hasColor = True
        self.__r = r
        self.__g = g
        self.__b = b

    cpdef void colorInt(self, int r, int g, int b):
        if self.__noColor:
            return

        if not self.__hasColor:
            self.__len += 3

        self.__hasColor = True
        self.__r = <float>(<char>r & 0xFF) / 255.0
        self.__g = <float>(<char>g & 0xFF) / 255.0
        self.__b = <float>(<char>b & 0xFF) / 255.0

    cpdef inline void vertexUV(self, float x, float y, float z, float u, float v):
        if not self.__hasTexture:
            self.__len += 2

        self.__hasTexture = True
        self.__u = u
        self.__v = v
        self.vertex(x, y, z)

    cpdef inline void vertex(self, float x, float y, float z):
        if self.__hasTexture:
            self.__array[self.__p] = self.__u
            self.__p += 1
            self.__array[self.__p] = self.__v
            self.__p += 1

        if self.__hasColor:
            self.__array[self.__p] = self.__r
            self.__p += 1
            self.__array[self.__p] = self.__g
            self.__p += 1
            self.__array[self.__p] = self.__b
            self.__p += 1

        self.__array[self.__p] = x
        self.__p += 1
        self.__array[self.__p] = y
        self.__p += 1
        self.__array[self.__p] = z
        self.__p += 1

        self.__vertices += 1
        if self.__vertices % 4 == 0 and self.__p >= self.max_floats - (self.__len << 2):
            self.end()

    cpdef void color(self, int c):
        cdef int r = c >> 16 & 0xFF
        cdef int g = c >> 8 & 0xFF
        cdef int b = c & 0xFF
        self.colorInt(r, g, b)

    cpdef inline void noColor(self):
        self.__noColor = True

tesselator = Tesselator()
