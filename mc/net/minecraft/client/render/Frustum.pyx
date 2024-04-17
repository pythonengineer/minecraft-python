# cython: language_level=3

from libc.math cimport sqrt

from mc.JavaUtils import BufferUtils
from pyglet import gl

cdef class Frustum:
    RIGHT = 0
    LEFT = 1
    BOTTOM = 2
    TOP = 3
    BACK = 4
    FRONT = 5
    A = 0
    B = 1
    C = 2
    D = 3

    def __cinit__(self):
        self._right = Frustum.RIGHT
        self._left = Frustum.LEFT
        self._bottom = Frustum.BOTTOM
        self._top = Frustum.TOP
        self._back = Frustum.BACK
        self._front = Frustum.FRONT
        self._a = Frustum.A
        self._b = Frustum.B
        self._c = Frustum.C
        self._d = Frustum.D

        self.__projectionMatrixBuffer = BufferUtils.createFloatBuffer(16)
        self.__modelviewMatrixBuffer = BufferUtils.createFloatBuffer(16)
        self.__clippingMatrixBuffer = BufferUtils.createFloatBuffer(16)
        for i in range(16):
            self.__projectionMatrix[i] = 0.0
            self.__modelviewMatrix[i] = 0.0
            self.__clippingMatrix[i] = 0.0

        for i in range(6):
            for n in range(4):
                self.__frustum[i][n] = 0.0

    def init(self):
        self.__projectionMatrixBuffer.clear()
        self.__modelviewMatrixBuffer.clear()
        self.__clippingMatrixBuffer.clear()

        proj = (gl.GLfloat * 16)()
        modl = (gl.GLfloat * 16)()
        gl.glGetFloatv(gl.GL_PROJECTION_MATRIX, proj)
        gl.glGetFloatv(gl.GL_MODELVIEW_MATRIX, modl)
        self.__projectionMatrixBuffer.putBytes(proj)
        self.__modelviewMatrixBuffer.putBytes(modl)

        self.__projectionMatrixBuffer.flip().limit(16)
        self.__projectionMatrixBuffer.getFloats(self.__projectionMatrix, 16)
        self.__modelviewMatrixBuffer.flip().limit(16)
        self.__modelviewMatrixBuffer.getFloats(self.__modelviewMatrix, 16)

        self.__clippingMatrix[0] = self.__modelviewMatrix[0] * self.__projectionMatrix[0] + self.__modelviewMatrix[1] * self.__projectionMatrix[4] + \
                                   self.__modelviewMatrix[2] * self.__projectionMatrix[8] + self.__modelviewMatrix[3] * self.__projectionMatrix[12]
        self.__clippingMatrix[1] = self.__modelviewMatrix[0] * self.__projectionMatrix[1] + self.__modelviewMatrix[1] * self.__projectionMatrix[5] + \
                                   self.__modelviewMatrix[2] * self.__projectionMatrix[9] + self.__modelviewMatrix[3] * self.__projectionMatrix[13]
        self.__clippingMatrix[2] = self.__modelviewMatrix[0] * self.__projectionMatrix[2] + self.__modelviewMatrix[1] * self.__projectionMatrix[6] + \
                                   self.__modelviewMatrix[2] * self.__projectionMatrix[10] + self.__modelviewMatrix[3] * self.__projectionMatrix[14]
        self.__clippingMatrix[3] = self.__modelviewMatrix[0] * self.__projectionMatrix[3] + self.__modelviewMatrix[1] * self.__projectionMatrix[7] + \
                                   self.__modelviewMatrix[2] * self.__projectionMatrix[11] + self.__modelviewMatrix[3] * self.__projectionMatrix[15]
        self.__clippingMatrix[4] = self.__modelviewMatrix[4] * self.__projectionMatrix[0] + self.__modelviewMatrix[5] * self.__projectionMatrix[4] + \
                                   self.__modelviewMatrix[6] * self.__projectionMatrix[8] + self.__modelviewMatrix[7] * self.__projectionMatrix[12]
        self.__clippingMatrix[5] = self.__modelviewMatrix[4] * self.__projectionMatrix[1] + self.__modelviewMatrix[5] * self.__projectionMatrix[5] + \
                                   self.__modelviewMatrix[6] * self.__projectionMatrix[9] + self.__modelviewMatrix[7] * self.__projectionMatrix[13]
        self.__clippingMatrix[6] = self.__modelviewMatrix[4] * self.__projectionMatrix[2] + self.__modelviewMatrix[5] * self.__projectionMatrix[6] + \
                                   self.__modelviewMatrix[6] * self.__projectionMatrix[10] + self.__modelviewMatrix[7] * self.__projectionMatrix[14]
        self.__clippingMatrix[7] = self.__modelviewMatrix[4] * self.__projectionMatrix[3] + self.__modelviewMatrix[5] * self.__projectionMatrix[7] + \
                                   self.__modelviewMatrix[6] * self.__projectionMatrix[11] + self.__modelviewMatrix[7] * self.__projectionMatrix[15]
        self.__clippingMatrix[8] = self.__modelviewMatrix[8] * self.__projectionMatrix[0] + self.__modelviewMatrix[9] * self.__projectionMatrix[4] + \
                                   self.__modelviewMatrix[10] * self.__projectionMatrix[8] + self.__modelviewMatrix[11] * self.__projectionMatrix[12]
        self.__clippingMatrix[9] = self.__modelviewMatrix[8] * self.__projectionMatrix[1] + self.__modelviewMatrix[9] * self.__projectionMatrix[5] + \
                                   self.__modelviewMatrix[10] * self.__projectionMatrix[9] + self.__modelviewMatrix[11] * self.__projectionMatrix[13]
        self.__clippingMatrix[10] = self.__modelviewMatrix[8] * self.__projectionMatrix[2] + self.__modelviewMatrix[9] * self.__projectionMatrix[6] + \
                                    self.__modelviewMatrix[10] * self.__projectionMatrix[10] + self.__modelviewMatrix[11] * self.__projectionMatrix[14]
        self.__clippingMatrix[11] = self.__modelviewMatrix[8] * self.__projectionMatrix[3] + self.__modelviewMatrix[9] * self.__projectionMatrix[7] + \
                                    self.__modelviewMatrix[10] * self.__projectionMatrix[11] + self.__modelviewMatrix[11] * self.__projectionMatrix[15]
        self.__clippingMatrix[12] = self.__modelviewMatrix[12] * self.__projectionMatrix[0] + self.__modelviewMatrix[13] * self.__projectionMatrix[4] + \
                                    self.__modelviewMatrix[14] * self.__projectionMatrix[8] + self.__modelviewMatrix[15] * self.__projectionMatrix[12]
        self.__clippingMatrix[13] = self.__modelviewMatrix[12] * self.__projectionMatrix[1] + self.__modelviewMatrix[13] * self.__projectionMatrix[5] + \
                                    self.__modelviewMatrix[14] * self.__projectionMatrix[9] + self.__modelviewMatrix[15] * self.__projectionMatrix[13]
        self.__clippingMatrix[14] = self.__modelviewMatrix[12] * self.__projectionMatrix[2] + self.__modelviewMatrix[13] * self.__projectionMatrix[6] + \
                                    self.__modelviewMatrix[14] * self.__projectionMatrix[10] + self.__modelviewMatrix[15] * self.__projectionMatrix[14]
        self.__clippingMatrix[15] = self.__modelviewMatrix[12] * self.__projectionMatrix[3] + self.__modelviewMatrix[13] * self.__projectionMatrix[7] + \
                                    self.__modelviewMatrix[14] * self.__projectionMatrix[11] + self.__modelviewMatrix[15] * self.__projectionMatrix[15]

        self.__frustum[self._right][self._a] = self.__clippingMatrix[3] - self.__clippingMatrix[0]
        self.__frustum[self._right][self._b] = self.__clippingMatrix[7] - self.__clippingMatrix[4]
        self.__frustum[self._right][self._c] = self.__clippingMatrix[11] - self.__clippingMatrix[8]
        self.__frustum[self._right][self._d] = self.__clippingMatrix[15] - self.__clippingMatrix[12]

        self.__normalize(self._right)

        self.__frustum[self._left][self._a] = self.__clippingMatrix[3] + self.__clippingMatrix[0]
        self.__frustum[self._left][self._b] = self.__clippingMatrix[7] + self.__clippingMatrix[4]
        self.__frustum[self._left][self._c] = self.__clippingMatrix[11] + self.__clippingMatrix[8]
        self.__frustum[self._left][self._d] = self.__clippingMatrix[15] + self.__clippingMatrix[12]

        self.__normalize(self._left)

        self.__frustum[self._bottom][self._a] = self.__clippingMatrix[3] + self.__clippingMatrix[1]
        self.__frustum[self._bottom][self._b] = self.__clippingMatrix[7] + self.__clippingMatrix[5]
        self.__frustum[self._bottom][self._c] = self.__clippingMatrix[11] + self.__clippingMatrix[9]
        self.__frustum[self._bottom][self._d] = self.__clippingMatrix[15] + self.__clippingMatrix[13]

        self.__normalize(self._bottom)

        self.__frustum[self._top][self._a] = self.__clippingMatrix[3] - self.__clippingMatrix[1]
        self.__frustum[self._top][self._b] = self.__clippingMatrix[7] - self.__clippingMatrix[5]
        self.__frustum[self._top][self._c] = self.__clippingMatrix[11] - self.__clippingMatrix[9]
        self.__frustum[self._top][self._d] = self.__clippingMatrix[15] - self.__clippingMatrix[13]

        self.__normalize(self._top)

        self.__frustum[self._back][self._a] = self.__clippingMatrix[3] - self.__clippingMatrix[2]
        self.__frustum[self._back][self._b] = self.__clippingMatrix[7] - self.__clippingMatrix[6]
        self.__frustum[self._back][self._c] = self.__clippingMatrix[11] - self.__clippingMatrix[10]
        self.__frustum[self._back][self._d] = self.__clippingMatrix[15] - self.__clippingMatrix[14]

        self.__normalize(self._back)

        self.__frustum[self._front][self._a] = self.__clippingMatrix[3] + self.__clippingMatrix[2]
        self.__frustum[self._front][self._b] = self.__clippingMatrix[7] + self.__clippingMatrix[6]
        self.__frustum[self._front][self._c] = self.__clippingMatrix[11] + self.__clippingMatrix[10]
        self.__frustum[self._front][self._d] = self.__clippingMatrix[15] + self.__clippingMatrix[14]

        self.__normalize(self._front)

        return self

    cdef __normalize(self, int side):
        cdef float magnitude = sqrt(self.__frustum[side][self._a] * self.__frustum[side][self._a] + \
                                    self.__frustum[side][self._b] * self.__frustum[side][self._b] + \
                                    self.__frustum[side][self._c] * self.__frustum[side][self._c])

        self.__frustum[side][self._a] /= magnitude
        self.__frustum[side][self._b] /= magnitude
        self.__frustum[side][self._c] /= magnitude
        self.__frustum[side][self._d] /= magnitude

    cpdef bint isBoundingBoxFullyInFrustum(self, float x0, float y0, float z0,
                                           float x1, float y1, float z1):
        for i in range(6):
            if not self.__frustum[i][self._a] * x0 + self.__frustum[i][self._b] * y0 + self.__frustum[i][self._c] * z0 + self.__frustum[i][self._d] > 0.0:
                return False
            if not self.__frustum[i][self._a] * x1 + self.__frustum[i][self._b] * y0 + self.__frustum[i][self._c] * z0 + self.__frustum[i][self._d] > 0.0:
                return False
            if not self.__frustum[i][self._a] * x0 + self.__frustum[i][self._b] * y1 + self.__frustum[i][self._c] * z0 + self.__frustum[i][self._d] > 0.0:
                return False
            if not self.__frustum[i][self._a] * x1 + self.__frustum[i][self._b] * y1 + self.__frustum[i][self._c] * z0 + self.__frustum[i][self._d] > 0.0:
                return False
            if not self.__frustum[i][self._a] * x0 + self.__frustum[i][self._b] * y0 + self.__frustum[i][self._c] * z1 + self.__frustum[i][self._d] > 0.0:
                return False
            if not self.__frustum[i][self._a] * x1 + self.__frustum[i][self._b] * y0 + self.__frustum[i][self._c] * z1 + self.__frustum[i][self._d] > 0.0:
                return False
            if not self.__frustum[i][self._a] * x0 + self.__frustum[i][self._b] * y1 + self.__frustum[i][self._c] * z1 + self.__frustum[i][self._d] > 0.0:
                return False
            if not self.__frustum[i][self._a] * x1 + self.__frustum[i][self._b] * y1 + self.__frustum[i][self._c] * z1 + self.__frustum[i][self._d] > 0.0:
                return False

        return True

    cpdef bint isBoundingBoxInFrustum(self, float x0, float y0, float z0,
                                      float x1, float y1, float z1):
        for i in range(6):
            if self.__frustum[i][self._a] * x0 + self.__frustum[i][self._b] * y0 + self.__frustum[i][self._c] * z0 + self.__frustum[i][self._d] <= 0.0 and \
               self.__frustum[i][self._a] * x1 + self.__frustum[i][self._b] * y0 + self.__frustum[i][self._c] * z0 + self.__frustum[i][self._d] <= 0.0 and \
               self.__frustum[i][self._a] * x0 + self.__frustum[i][self._b] * y1 + self.__frustum[i][self._c] * z0 + self.__frustum[i][self._d] <= 0.0 and \
               self.__frustum[i][self._a] * x1 + self.__frustum[i][self._b] * y1 + self.__frustum[i][self._c] * z0 + self.__frustum[i][self._d] <= 0.0 and \
               self.__frustum[i][self._a] * x0 + self.__frustum[i][self._b] * y0 + self.__frustum[i][self._c] * z1 + self.__frustum[i][self._d] <= 0.0 and \
               self.__frustum[i][self._a] * x1 + self.__frustum[i][self._b] * y0 + self.__frustum[i][self._c] * z1 + self.__frustum[i][self._d] <= 0.0 and \
               self.__frustum[i][self._a] * x0 + self.__frustum[i][self._b] * y1 + self.__frustum[i][self._c] * z1 + self.__frustum[i][self._d] <= 0.0 and \
               self.__frustum[i][self._a] * x1 + self.__frustum[i][self._b] * y1 + self.__frustum[i][self._c] * z1 + self.__frustum[i][self._d] <= 0.0:
                return False

        return True

    cpdef bint isVisible(self, aabb):
        return self.isBoundingBoxInFrustum(aabb.minX, aabb.minY, aabb.minZ,
                                           aabb.maxX, aabb.maxY, aabb.maxZ)
