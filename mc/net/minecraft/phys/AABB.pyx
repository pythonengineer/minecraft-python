# cython: language_level=3

cimport cython

from pyglet import gl

@cython.final
cdef class AABB:

    def __cinit__(self):
        self.__epsilon = 0.0

    def __init__(self, x0, y0, z0, x1, y1, z1):
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1

    cpdef AABB expand(self, float xa, float ya, float za):
        _x0 = self.x0
        _y0 = self.y0
        _z0 = self.z0
        _x1 = self.x1
        _y1 = self.y1
        _z1 = self.z1

        if xa < 0.0: _x0 += xa
        if xa > 0.0: _x1 += xa
        if ya < 0.0: _y0 += ya
        if ya > 0.0: _y1 += ya
        if za < 0.0: _z0 += za
        if za > 0.0: _z1 += za

        return AABB(_x0, _y0, _z0, _x1, _y1, _z1)

    def grow(self, xa, ya, za):
        _x0 = self.x0 - xa
        _y0 = self.y0 - ya
        _z0 = self.z0 - za
        _x1 = self.x1 + xa
        _y1 = self.y1 + ya
        _z1 = self.z1 + za

        return AABB(_x0, _y0, _z0, _x1, _y1, _z1)

    def cloneMove(self, xa, ya, za):
        return AABB(self.x0 + za, self.y0 + ya, self.z0 + za, self.x1 + xa, self.y1 + ya, self.z1 + za)

    cdef float clipXCollide(self, AABB c, float xa):
        cdef float maximum

        if c.y1 <= self.y0 or c.y0 >= self.y1:
            return xa
        if c.z1 <= self.z0 or c.z0 >= self.z1:
            return xa

        if xa > 0.0 and c.x1 <= self.x0:
            maximum = self.x0 - c.x1 - self.__epsilon
            if maximum < xa:
                xa = maximum

        if xa < 0.0 and c.x0 >= self.x1:
            maximum = self.x1 - c.x0 + self.__epsilon
            if maximum > xa:
                xa = maximum

        return xa

    cdef float clipYCollide(self, AABB c, float ya):
        cdef float maximum

        if c.x1 <= self.x0 or c.x0 >= self.x1:
            return ya
        if c.z1 <= self.z0 or c.z0 >= self.z1:
            return ya

        if ya > 0.0 and c.y1 <= self.y0:
            maximum = self.y0 - c.y1 - self.__epsilon
            if maximum < ya:
                ya = maximum

        if ya < 0.0 and c.y0 >= self.y1:
            maximum = self.y1 - c.y0 + self.__epsilon
            if maximum > ya:
                ya = maximum

        return ya

    cdef float clipZCollide(self, AABB c, float za):
        cdef float maximum

        if c.x1 <= self.x0 or c.x0 >= self.x1:
            return za
        if c.y1 <= self.y0 or c.y0 >= self.y1:
            return za

        if za > 0.0 and c.z1 <= self.z0:
            maximum = self.z0 - c.z1 - self.__epsilon
            if maximum < za:
                za = maximum

        if za < 0.0 and c.z0 >= self.z1:
            maximum = self.z1 - c.z0 + self.__epsilon
            if maximum > za:
                za = maximum

        return za

    def intersectsBB(self, c):
        if c.x1 <= self.x0 or c.x0 >= self.x1:
            return False
        if c.y1 <= self.y0 or c.y0 >= self.y1:
            return False
        if c.z1 <= self.x0 or c.z0 >= self.x1:
            return False

        return True

    def intersectsInner(self, c):
        if c.x1 >= self.x0 and c.x0 <= self.x1:
            if c.y1 >= self.y0 and c.y0 <= self.y1:
                return c.z1 >= self.z0 and c.z0 <= self.z1

        return False

    cpdef void move(self, float xa, float ya, float za):
        self.x0 += xa
        self.y0 += ya
        self.z0 += za
        self.x1 += xa
        self.y1 += ya
        self.z1 += za

    def intersects(self, minX, minY, minZ, maxX, maxY, maxZ):
        if maxX <= self.x0 or minX >= self.x1:
            return False
        if maxY <= self.y0 or minY >= self.y1:
            return False
        if maxZ <= self.z0 or minZ >= self.z1:
            return False

        return True

    def contains(self, vec):
        if vec.x <= self.x0 or vec.x >= self.x1:
            return False

        if vec.y <= self.y0 or vec.y >= self.y1:
            return False

        return not (vec.z <= self.z0) and not (vec.z >= self.z1)

    def render(self):
        gl.glBegin(gl.GL_LINE_STRIP)
        gl.glVertex3f(self.x0, self.y0, self.z0)
        gl.glVertex3f(self.x1, self.y0, self.z0)
        gl.glVertex3f(self.x1, self.y0, self.z1)
        gl.glVertex3f(self.x0, self.y0, self.z1)
        gl.glVertex3f(self.x0, self.y0, self.z0)
        gl.glEnd()
        gl.glBegin(gl.GL_LINE_STRIP)
        gl.glVertex3f(self.x0, self.y1, self.z0)
        gl.glVertex3f(self.x1, self.y1, self.z0)
        gl.glVertex3f(self.x1, self.y1, self.z1)
        gl.glVertex3f(self.x0, self.y1, self.z1)
        gl.glVertex3f(self.x0, self.y1, self.z0)
        gl.glEnd()
        gl.glBegin(gl.GL_LINES)
        gl.glVertex3f(self.x0, self.y0, self.z0)
        gl.glVertex3f(self.x0, self.y1, self.z0)
        gl.glVertex3f(self.x1, self.y0, self.z0)
        gl.glVertex3f(self.x1, self.y1, self.z0)
        gl.glVertex3f(self.x1, self.y0, self.z1)
        gl.glVertex3f(self.x1, self.y1, self.z1)
        gl.glVertex3f(self.x0, self.y0, self.z1)
        gl.glVertex3f(self.x0, self.y1, self.z1)
        gl.glEnd()

    def getSize(self):
        xd = self.x1 - self.x0
        yd = self.y1 - self.y0
        zd = self.z1 - self.z0
        return (xd + yd + zd) / 3.0

    def shrink(self, xa, ya, za):
        x0 = self.x0
        y0 = self.y0
        z0 = self.z0
        x1 = self.x1
        y1 = self.y1
        z1 = self.z1
        if xa < 0.0:
            x0 -= xa
        if xa > 0.0:
            x1 -= xa
        if ya < 0.0:
            y0 -= ya
        if ya > 0.0:
            y1 -= ya
        if za < 0.0:
            z0 -= za
        if za > 0.0:
            z1 -= za

        return AABB(x0, y0, z0, x1, y1, z1)

    cdef AABB copy(self):
        return AABB(self.x0, self.y0, self.z0, self.x1, self.y1, self.z1)
