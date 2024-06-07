# cython: language_level=3

import numpy as np
cimport numpy as np

from mc.JavaUtils cimport floatToRawIntBits
from mc.JavaUtils import BufferUtils
from pyglet import gl

cdef class Tessellator:
    MAX_INTS = 2097152

    def __cinit__(self):
        self.max_ints = self.MAX_INTS
        self.__byteBuffer = BufferUtils.createIntBuffer(self.max_ints)
        self.__rawBuffer = np.zeros(self.max_ints, dtype=np.int32)
        self.__colors = 3

    cpdef void draw(self):
        if self.__vertexCount > 0:
            self.__byteBuffer.clear()
            self.__byteBuffer.putInts(self.__rawBuffer, 0, self.__addedVertices)
            self.__byteBuffer.flip()

            if self.__hasTexture and self.__hasColor:
                self.__byteBuffer.glInterleavedArrays(gl.GL_T2F_C4UB_V3F, 0)
            elif self.__hasTexture:
                self.__byteBuffer.glInterleavedArrays(gl.GL_T2F_V3F, 0)
            elif self.__hasColor:
                self.__byteBuffer.glInterleavedArrays(gl.GL_C4UB_V3F, 0)
            else:
                self.__byteBuffer.glInterleavedArrays(gl.GL_V3F, 0)

            gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
            if self.__hasTexture:
                gl.glEnableClientState(gl.GL_TEXTURE_COORD_ARRAY)
            if self.__hasColor:
                gl.glEnableClientState(gl.GL_COLOR_ARRAY)

            gl.glDrawArrays(gl.GL_QUADS, gl.GL_POINTS, self.__vertexCount)

            gl.glDisableClientState(gl.GL_VERTEX_ARRAY)
            if self.__hasTexture:
                gl.glDisableClientState(gl.GL_TEXTURE_COORD_ARRAY)
            if self.__hasColor:
                gl.glDisableClientState(gl.GL_COLOR_ARRAY)

        self.__reset()

    cdef void __reset(self):
        self.__vertexCount = 0
        self.__byteBuffer.clear()
        self.__addedVertices = 0
        self.__rawBufferIndex = 0
        self.__colors = 3

    cpdef void startDrawingQuads(self):
        if self.__vertexCount > 0:
            raise RuntimeError('OMG ALREADY VERTICES!')

        self.__reset()
        self.__hasColor = False
        self.__hasTexture = False
        self.__drawMode = False

    cpdef inline void setColorOpaque_F(self, float r, float g, float b):
        self.__setColorOpaque(<int>(r * 255.0), <int>(g * 255.0), <int>(b * 255.0))

    cdef inline void __setColorOpaque(self, int r, int g, int b):
        if self.__drawMode:
            return

        if not self.__hasColor:
            self.__colors += 1

        r = max(min(r, 255), 0)
        g = max(min(g, 255), 0)
        b = max(min(b, 255), 0)

        self.__hasColor = True
        self.__color = -16777216 | b << 16 | g << 8 | r

    cpdef void addVertexWithUV(self, float x, float y, float z, float u, float v):
        if not self.__hasTexture:
            self.__colors += 2

        self.__hasTexture = True
        self.__textureU = u
        self.__textureV = v
        self.addVertex(x, y, z)

    cpdef void addVertex(self, float x, float y, float z):
        self.__rawBufferIndex += 1
        if self.__hasTexture:
            self.__rawBuffer[self.__addedVertices] = floatToRawIntBits(self.__textureU)
            self.__addedVertices += 1
            self.__rawBuffer[self.__addedVertices] = floatToRawIntBits(self.__textureV)
            self.__addedVertices += 1

        if self.__hasColor:
            self.__rawBuffer[self.__addedVertices] = self.__color
            self.__addedVertices += 1

        self.__rawBuffer[self.__addedVertices] = floatToRawIntBits(x)
        self.__addedVertices += 1
        self.__rawBuffer[self.__addedVertices] = floatToRawIntBits(y)
        self.__addedVertices += 1
        self.__rawBuffer[self.__addedVertices] = floatToRawIntBits(z)
        self.__addedVertices += 1

        self.__vertexCount += 1
        if self.__vertexCount % 4 == 0 and self.__addedVertices >= self.max_ints - (self.__colors << 2):
            self.draw()

    cpdef inline void setColorOpaque_I(self, int c):
        cdef int r = c >> 16 & 0xFF
        cdef int g = c >> 8 & 0xFF
        cdef int b = c & 0xFF
        self.__setColorOpaque(r, g, b)

    cpdef inline void disableColor(self):
        self.__drawMode = True

    @staticmethod
    def setNormal(float x, float y, float z):
        gl.glNormal3f(x, y, z)

tessellator = Tessellator()
