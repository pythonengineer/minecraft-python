# cython: language_level=3

from mc.net.minecraft.game.physics.MovingObjectPosition import MovingObjectPosition
from pyglet import gl

cdef class AxisAlignedBB:

    def __cinit__(self):
        self.__epsilon = 0.0

    def __init__(self, x0, y0, z0, x1, y1, z1):
        self.minX = x0
        self.minY = y0
        self.minZ = z0
        self.maxX = x1
        self.maxY = y1
        self.maxZ = z1

    cpdef AxisAlignedBB addCoord(self, float xa, float ya, float za):
        _x0 = self.minX
        _y0 = self.minY
        _z0 = self.minZ
        _x1 = self.maxX
        _y1 = self.maxY
        _z1 = self.maxZ

        if xa < 0.0: _x0 += xa
        if xa > 0.0: _x1 += xa
        if ya < 0.0: _y0 += ya
        if ya > 0.0: _y1 += ya
        if za < 0.0: _z0 += za
        if za > 0.0: _z1 += za

        return AxisAlignedBB(_x0, _y0, _z0, _x1, _y1, _z1)

    def expand(self, xa, ya, za):
        _x0 = self.minX - xa
        _y0 = self.minY - ya
        _z0 = self.minZ - za
        _x1 = self.maxX + xa
        _y1 = self.maxY + ya
        _z1 = self.maxZ + za

        return AxisAlignedBB(_x0, _y0, _z0, _x1, _y1, _z1)

    def cloneMove(self, xa, ya, za):
        return AxisAlignedBB(self.minX + za, self.minY + ya, self.minZ + za,
                             self.maxX + xa, self.maxY + ya, self.maxZ + za)

    cdef float calculateXOffset(self, AxisAlignedBB c, float xa):
        cdef float maximum

        if c.maxY <= self.minY or c.minY >= self.maxY:
            return xa
        if c.maxZ <= self.minZ or c.minZ >= self.maxZ:
            return xa

        if xa > 0.0 and c.maxX <= self.minX:
            maximum = self.minX - c.maxX
            if maximum < xa:
                xa = maximum

        if xa < 0.0 and c.minX >= self.maxX:
            maximum = self.maxX - c.minX
            if maximum > xa:
                xa = maximum

        return xa

    cdef float calculateYOffset(self, AxisAlignedBB c, float ya):
        cdef float maximum

        if c.maxX <= self.minX or c.minX >= self.maxX:
            return ya
        if c.maxZ <= self.minZ or c.minZ >= self.maxZ:
            return ya

        if ya > 0.0 and c.maxY <= self.minY:
            maximum = self.minY - c.maxY
            if maximum < ya:
                ya = maximum

        if ya < 0.0 and c.minY >= self.maxY:
            maximum = self.maxY - c.minY
            if maximum > ya:
                ya = maximum

        return ya

    cdef float calculateZOffset(self, AxisAlignedBB c, float za):
        cdef float maximum

        if c.maxX <= self.minX or c.minX >= self.maxX:
            return za
        if c.maxY <= self.minY or c.minY >= self.maxY:
            return za

        if za > 0.0 and c.maxZ <= self.minZ:
            maximum = self.minZ - c.maxZ
            if maximum < za:
                za = maximum

        if za < 0.0 and c.minZ >= self.maxZ:
            maximum = self.maxZ - c.minZ
            if maximum > za:
                za = maximum

        return za

    def intersectsBB(self, c):
        if c.maxX <= self.minX or c.minX >= self.maxX:
            return False
        if c.maxY <= self.minY or c.minY >= self.maxY:
            return False
        if c.maxZ <= self.minX or c.minZ >= self.maxX:
            return False

        return True

    def intersectsWith(self, c):
        if c.maxX >= self.minX and c.minX <= self.maxX:
            if c.maxY >= self.minY and c.minY <= self.maxY:
                return c.maxZ >= self.minZ and c.minZ <= self.maxZ

        return False

    cpdef void offset(self, float xa, float ya, float za):
        self.minX += xa
        self.minY += ya
        self.minZ += za
        self.maxX += xa
        self.maxY += ya
        self.maxZ += za

    cdef AxisAlignedBB copy(self):
        return AxisAlignedBB(self.minX, self.minY, self.minZ, self.maxX, self.maxY, self.maxZ)

    def intersects(self, minX, minY, minZ, maxX, maxY, maxZ):
        if maxX <= self.minX or minX >= self.maxX:
            return False
        if maxY <= self.minY or minY >= self.maxY:
            return False
        if maxZ <= self.minZ or minZ >= self.maxZ:
            return False

        return True

    def render(self):
        gl.glBegin(gl.GL_LINE_STRIP)
        gl.glVertex3f(self.minX, self.minY, self.minZ)
        gl.glVertex3f(self.maxX, self.minY, self.minZ)
        gl.glVertex3f(self.maxX, self.minY, self.maxZ)
        gl.glVertex3f(self.minX, self.minY, self.maxZ)
        gl.glVertex3f(self.minX, self.minY, self.minZ)
        gl.glEnd()
        gl.glBegin(gl.GL_LINE_STRIP)
        gl.glVertex3f(self.minX, self.maxY, self.minZ)
        gl.glVertex3f(self.maxX, self.maxY, self.minZ)
        gl.glVertex3f(self.maxX, self.maxY, self.maxZ)
        gl.glVertex3f(self.minX, self.maxY, self.maxZ)
        gl.glVertex3f(self.minX, self.maxY, self.minZ)
        gl.glEnd()
        gl.glBegin(gl.GL_LINES)
        gl.glVertex3f(self.minX, self.minY, self.minZ)
        gl.glVertex3f(self.minX, self.maxY, self.minZ)
        gl.glVertex3f(self.maxX, self.minY, self.minZ)
        gl.glVertex3f(self.maxX, self.maxY, self.minZ)
        gl.glVertex3f(self.maxX, self.minY, self.maxZ)
        gl.glVertex3f(self.maxX, self.maxY, self.maxZ)
        gl.glVertex3f(self.minX, self.minY, self.maxZ)
        gl.glVertex3f(self.minX, self.maxY, self.maxZ)
        gl.glEnd()

    def getSize(self):
        xd = self.maxX - self.minX
        yd = self.maxY - self.minY
        zd = self.maxZ - self.minZ
        return (xd + yd + zd) / 3.0

    cpdef calculateIntercept(self, vec1, vec2):
        cdef char b

        vecX0 = vec1.getIntermediateWithXValue(vec2, self.minX)
        vecX1 = vec1.getIntermediateWithXValue(vec2, self.maxX)
        vecY0 = vec1.getIntermediateWithYValue(vec2, self.minY)
        vecY1 = vec1.getIntermediateWithYValue(vec2, self.maxY)
        vecZ0 = vec1.getIntermediateWithZValue(vec2, self.minZ)
        vecZ1 = vec1.getIntermediateWithZValue(vec2, self.maxZ)
        if not self.__isVecInYZ(vecX0):
            vecX0 = None
        if not self.__isVecInYZ(vecX1):
            vecX1 = None
        if not self.__isVecInXZ(vecY0):
            vecY0 = None
        if not self.__isVecInXZ(vecY1):
            vecY1 = None
        if not self.__isVecInXY(vecZ0):
            vecZ0 = None
        if not self.__isVecInXY(vecZ1):
            vecZ1 = None

        vec38 = None
        if vecX0:
            vec38 = vecX0

        if vecX1 and (not vec38 or vec1.squaredDistanceTo(vecX1) < vec1.squaredDistanceTo(vec38)):
            vec38 = vecX1
        if vecY0 and (not vec38 or vec1.squaredDistanceTo(vecY0) < vec1.squaredDistanceTo(vec38)):
            vec38 = vecY0
        if vecY1 and (not vec38 or vec1.squaredDistanceTo(vecY1) < vec1.squaredDistanceTo(vec38)):
            vec38 = vecY1
        if vecZ0 and (not vec38 or vec1.squaredDistanceTo(vecZ0) < vec1.squaredDistanceTo(vec38)):
            vec38 = vecZ0
        if vecZ1 and (not vec38 or vec1.squaredDistanceTo(vecZ1) < vec1.squaredDistanceTo(vec38)):
            vec38 = vecZ1

        if not vec38:
            return

        b = -1
        if vec38 == vecX0:
            b = 4
        elif vec38 == vecX1:
            b = 5
        elif vec38 == vecY0:
            b = 0
        elif vec38 == vecY1:
            b = 1
        elif vec38 == vecZ0:
            b = 2
        elif vec38 == vecZ1:
            b = 3

        return MovingObjectPosition(0, 0, 0, b, vec38)

    cdef bint __isVecInYZ(self, xa):
        return False if not xa else xa.yCoord >= self.minY and xa.yCoord <= self.maxY and \
               xa.zCoord >= self.minZ and xa.zCoord <= self.maxZ

    cdef bint __isVecInXZ(self, ya):
        return False if not ya else ya.xCoord >= self.minX and ya.xCoord <= self.maxX and \
               ya.zCoord >= self.minZ and ya.zCoord <= self.maxZ

    cdef bint __isVecInXY(self, za):
        return False if not za else za.xCoord >= self.minX and za.xCoord <= self.maxX and \
               za.yCoord >= self.minY and za.yCoord <= self.maxY
