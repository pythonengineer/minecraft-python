# cython: language_level=3

from libc.math cimport sqrt

from mc.CompatibilityShims import BufferUtils
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

        self._proj = BufferUtils.createFloatBuffer(16)
        self._modl = BufferUtils.createFloatBuffer(16)
        self._clip = BufferUtils.createFloatBuffer(16)
        for i in range(16):
            self.__proj[i] = 0.0
            self.__modl[i] = 0.0
            self.__clip[i] = 0.0

        self.calculateFrustum()

    cpdef void calculateFrustum(self):
        for i in range(6):
            for n in range(4):
                self.__m_Frustum[i][n] = 0.0

        self._proj.clear()
        self._modl.clear()
        self._clip.clear()

        gl.glGetFloatv(gl.GL_PROJECTION_MATRIX, self._proj)
        gl.glGetFloatv(gl.GL_MODELVIEW_MATRIX, self._modl)

        proj = [0.0] * 16
        modl = [0.0] * 16

        for i in range(16):
            proj[i] = self.__proj[i]
            modl[i] = self.__modl[i]

        self._proj.flip().limit(16)
        self._proj.get(proj)
        self._modl.flip().limit(16)
        self._modl.get(modl)

        for i in range(16):
            self.__proj[i] = proj[i]
            self.__modl[i] = modl[i]

        self.__clip[0] = self.__modl[0] * self.__proj[0] + self.__modl[1] * self.__proj[4] + \
                         self.__modl[2] * self.__proj[8] + self.__modl[3] * self.__proj[12]
        self.__clip[1] = self.__modl[0] * self.__proj[1] + self.__modl[1] * self.__proj[5] + \
                         self.__modl[2] * self.__proj[9] + self.__modl[3] * self.__proj[13]
        self.__clip[2] = self.__modl[0] * self.__proj[2] + self.__modl[1] * self.__proj[6] + \
                         self.__modl[2] * self.__proj[10] + self.__modl[3] * self.__proj[14]
        self.__clip[3] = self.__modl[0] * self.__proj[3] + self.__modl[1] * self.__proj[7] + \
                         self.__modl[2] * self.__proj[11] + self.__modl[3] * self.__proj[15]
        self.__clip[4] = self.__modl[4] * self.__proj[0] + self.__modl[5] * self.__proj[4] + \
                         self.__modl[6] * self.__proj[8] + self.__modl[7] * self.__proj[12]
        self.__clip[5] = self.__modl[4] * self.__proj[1] + self.__modl[5] * self.__proj[5] + \
                         self.__modl[6] * self.__proj[9] + self.__modl[7] * self.__proj[13]
        self.__clip[6] = self.__modl[4] * self.__proj[2] + self.__modl[5] * self.__proj[6] + \
                         self.__modl[6] * self.__proj[10] + self.__modl[7] * self.__proj[14]
        self.__clip[7] = self.__modl[4] * self.__proj[3] + self.__modl[5] * self.__proj[7] + \
                         self.__modl[6] * self.__proj[11] + self.__modl[7] * self.__proj[15]
        self.__clip[8] = self.__modl[8] * self.__proj[0] + self.__modl[9] * self.__proj[4] + \
                         self.__modl[10] * self.__proj[8] + self.__modl[11] * self.__proj[12]
        self.__clip[9] = self.__modl[8] * self.__proj[1] + self.__modl[9] * self.__proj[5] + \
                         self.__modl[10] * self.__proj[9] + self.__modl[11] * self.__proj[13]
        self.__clip[10] = self.__modl[8] * self.__proj[2] + self.__modl[9] * self.__proj[6] + \
                          self.__modl[10] * self.__proj[10] + self.__modl[11] * self.__proj[14]
        self.__clip[11] = self.__modl[8] * self.__proj[3] + self.__modl[9] * self.__proj[7] + \
                          self.__modl[10] * self.__proj[11] + self.__modl[11] * self.__proj[15]
        self.__clip[12] = self.__modl[12] * self.__proj[0] + self.__modl[13] * self.__proj[4] + \
                          self.__modl[14] * self.__proj[8] + self.__modl[15] * self.__proj[12]
        self.__clip[13] = self.__modl[12] * self.__proj[1] + self.__modl[13] * self.__proj[5] + \
                          self.__modl[14] * self.__proj[9] + self.__modl[15] * self.__proj[13]
        self.__clip[14] = self.__modl[12] * self.__proj[2] + self.__modl[13] * self.__proj[6] + \
                          self.__modl[14] * self.__proj[10] + self.__modl[15] * self.__proj[14]
        self.__clip[15] = self.__modl[12] * self.__proj[3] + self.__modl[13] * self.__proj[7] + \
                          self.__modl[14] * self.__proj[11] + self.__modl[15] * self.__proj[15]

        self.__m_Frustum[self._right][self._a] = self.__clip[3] - self.__clip[0]
        self.__m_Frustum[self._right][self._b] = self.__clip[7] - self.__clip[4]
        self.__m_Frustum[self._right][self._c] = self.__clip[11] - self.__clip[8]
        self.__m_Frustum[self._right][self._d] = self.__clip[15] - self.__clip[12]

        self.__normalizePlane(self._right)

        self.__m_Frustum[self._left][self._a] = self.__clip[3] + self.__clip[0]
        self.__m_Frustum[self._left][self._b] = self.__clip[7] + self.__clip[4]
        self.__m_Frustum[self._left][self._c] = self.__clip[11] + self.__clip[8]
        self.__m_Frustum[self._left][self._d] = self.__clip[15] + self.__clip[12]

        self.__normalizePlane(self._left)

        self.__m_Frustum[self._bottom][self._a] = self.__clip[3] + self.__clip[1]
        self.__m_Frustum[self._bottom][self._b] = self.__clip[7] + self.__clip[5]
        self.__m_Frustum[self._bottom][self._c] = self.__clip[11] + self.__clip[9]
        self.__m_Frustum[self._bottom][self._d] = self.__clip[15] + self.__clip[13]

        self.__normalizePlane(self._bottom)

        self.__m_Frustum[self._top][self._a] = self.__clip[3] - self.__clip[1]
        self.__m_Frustum[self._top][self._b] = self.__clip[7] - self.__clip[5]
        self.__m_Frustum[self._top][self._c] = self.__clip[11] - self.__clip[9]
        self.__m_Frustum[self._top][self._d] = self.__clip[15] - self.__clip[13]

        self.__normalizePlane(self._top)

        self.__m_Frustum[self._back][self._a] = self.__clip[3] - self.__clip[2]
        self.__m_Frustum[self._back][self._b] = self.__clip[7] - self.__clip[6]
        self.__m_Frustum[self._back][self._c] = self.__clip[11] - self.__clip[10]
        self.__m_Frustum[self._back][self._d] = self.__clip[15] - self.__clip[14]

        self.__normalizePlane(self._back)

        self.__m_Frustum[self._front][self._a] = self.__clip[3] + self.__clip[2]
        self.__m_Frustum[self._front][self._b] = self.__clip[7] + self.__clip[6]
        self.__m_Frustum[self._front][self._c] = self.__clip[11] + self.__clip[10]
        self.__m_Frustum[self._front][self._d] = self.__clip[15] + self.__clip[14]

        self.__normalizePlane(self._front)

    cdef __normalizePlane(self, int side):
        cdef float magnitude = sqrt(self.__m_Frustum[side][self._a] * self.__m_Frustum[side][self._a] + \
                                    self.__m_Frustum[side][self._b] * self.__m_Frustum[side][self._b] + \
                                    self.__m_Frustum[side][self._c] * self.__m_Frustum[side][self._c])

        self.__m_Frustum[side][self._a] /= magnitude
        self.__m_Frustum[side][self._b] /= magnitude
        self.__m_Frustum[side][self._c] /= magnitude
        self.__m_Frustum[side][self._d] /= magnitude

    cdef bint cubeInFrustum(self, float x0, float y0, float z0,
                            float x1, float y1, float z1):
        cdef int i

        for i in range(6):
            if self.__m_Frustum[i][self._a] * x0 + self.__m_Frustum[i][self._b] * y0 + self.__m_Frustum[i][self._c] * z0 + self.__m_Frustum[i][self._d] <= 0.0 and \
               self.__m_Frustum[i][self._a] * x1 + self.__m_Frustum[i][self._b] * y0 + self.__m_Frustum[i][self._c] * z0 + self.__m_Frustum[i][self._d] <= 0.0 and \
               self.__m_Frustum[i][self._a] * x0 + self.__m_Frustum[i][self._b] * y1 + self.__m_Frustum[i][self._c] * z0 + self.__m_Frustum[i][self._d] <= 0.0 and \
               self.__m_Frustum[i][self._a] * x1 + self.__m_Frustum[i][self._b] * y1 + self.__m_Frustum[i][self._c] * z0 + self.__m_Frustum[i][self._d] <= 0.0 and \
               self.__m_Frustum[i][self._a] * x0 + self.__m_Frustum[i][self._b] * y0 + self.__m_Frustum[i][self._c] * z1 + self.__m_Frustum[i][self._d] <= 0.0 and \
               self.__m_Frustum[i][self._a] * x1 + self.__m_Frustum[i][self._b] * y0 + self.__m_Frustum[i][self._c] * z1 + self.__m_Frustum[i][self._d] <= 0.0 and \
               self.__m_Frustum[i][self._a] * x0 + self.__m_Frustum[i][self._b] * y1 + self.__m_Frustum[i][self._c] * z1 + self.__m_Frustum[i][self._d] <= 0.0 and \
               self.__m_Frustum[i][self._a] * x1 + self.__m_Frustum[i][self._b] * y1 + self.__m_Frustum[i][self._c] * z1 + self.__m_Frustum[i][self._d] <= 0.0:
                return False

        return True

    cpdef bint isVisible(self, object aabb):
        return self.cubeInFrustum(aabb.x0, aabb.y0, aabb.z0, aabb.x1, aabb.y1, aabb.z1)
