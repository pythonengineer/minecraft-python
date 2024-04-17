# cython: language_level=3

from mc.JavaUtils import BufferUtils
from pyglet import gl

cdef class Tessellator:
    MAX_FLOATS = 524288

    def __cinit__(self):
        self.max_floats = self.MAX_FLOATS
        self.__floatBuffer = BufferUtils.createFloatBuffer(self.max_floats)
        self.__colors = 3

    cpdef void draw(self):
        if self.__vertexCount > 0:
            self.__floatBuffer.clear()
            self.__floatBuffer.putFloats(self.__rawBuffer, 0, self.__addedVertices)
            self.__floatBuffer.flip()

            if self.__hasTexture and self.__hasColor:
                self.__floatBuffer.glInterleavedArrays(gl.GL_T2F_C3F_V3F, 0)
            elif self.__hasTexture:
                self.__floatBuffer.glInterleavedArrays(gl.GL_T2F_V3F, 0)
            elif self.__hasColor:
                self.__floatBuffer.glInterleavedArrays(gl.GL_C3F_V3F, 0)
            else:
                self.__floatBuffer.glInterleavedArrays(gl.GL_V3F, 0)

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
        self.__floatBuffer.clear()
        self.__addedVertices = 0

    cpdef void startDrawingQuads(self):
        if self.__vertexCount > 0:
            raise RuntimeError('OMG ALREADY VERTICES!')

        self.__reset()
        self.__hasColor = False
        self.__hasTexture = False
        self.__drawMode = False

    cpdef inline void setColorOpaque_F(self, float r, float g, float b):
        if self.__drawMode:
            return

        if not self.__hasColor:
            self.__colors += 3

        self.__hasColor = True
        self.__red = r
        self.__green = g
        self.__blue = b

    cpdef void addVertexWithUV(self, float x, float y, float z, float u, float v):
        if not self.__hasTexture:
            self.__colors += 2

        self.__hasTexture = True
        self.__textureU = u
        self.__textureV = v
        self.addVertex(x, y, z)

    cpdef void addVertex(self, float x, float y, float z):
        if self.__hasTexture:
            self.__rawBuffer[self.__addedVertices] = self.__textureU
            self.__addedVertices += 1
            self.__rawBuffer[self.__addedVertices] = self.__textureV
            self.__addedVertices += 1

        if self.__hasColor:
            self.__rawBuffer[self.__addedVertices] = self.__red
            self.__addedVertices += 1
            self.__rawBuffer[self.__addedVertices] = self.__green
            self.__addedVertices += 1
            self.__rawBuffer[self.__addedVertices] = self.__blue
            self.__addedVertices += 1

        self.__rawBuffer[self.__addedVertices] = x
        self.__addedVertices += 1
        self.__rawBuffer[self.__addedVertices] = y
        self.__addedVertices += 1
        self.__rawBuffer[self.__addedVertices] = z
        self.__addedVertices += 1

        self.__vertexCount += 1
        if self.__vertexCount % 4 == 0 and self.__addedVertices >= self.max_floats - (self.__colors << 2):
            self.draw()

    cpdef inline void setColorOpaque_I(self, int c):
        cdef char r = c >> 16 & 0xFF
        cdef char g = c >> 8 & 0xFF
        cdef char b = c & 0xFF
        if self.__drawMode:
            return

        if not self.__hasColor:
            self.__colors += 3

        self.__hasColor = True
        self.__red = <float>(r & 0xFF) / 255.0
        self.__green = <float>(g & 0xFF) / 255.0
        self.__blue = <float>(b & 0xFF) / 255.0

    cpdef inline void enableDrawMode(self):
        self.__drawMode = True

    @staticmethod
    def setNormal(float x, float y, float z):
        gl.glNormal3f(x, y, z)

tessellator = Tessellator()
