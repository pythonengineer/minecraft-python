# cython: language_level=3

from mc.net.minecraft.renderer.Tesselator cimport Tesselator
from mc.net.minecraft.renderer.Tesselator import tesselator
from mc.net.minecraft.level.Level cimport Level
from mc.net.minecraft.level.tile.Tiles import tiles
from mc.net.minecraft.phys.AABB import AABB
from mc.CompatibilityShims import getMillis
from pyglet import gl

cdef int Chunk_updates = 0
cdef int Chunk_totalUpdates = 0

cdef class Chunk:

    cdef:
        Level __level
        Tesselator __t

        int __x0
        int __y0
        int __z0
        int __x1
        int __y1
        int __z1

        float __x
        float __y
        float __z

        public object aabb
        int __lists
        bint __dirty
        public bint visible
        public bint canRender

    property updates:

        def __get__(self):
            return Chunk_updates

        def __set__(self, x):
            global Chunk_updates
            Chunk_updates = x

    property totalUpdates:

        def __get__(self):
            return Chunk_totalUpdates

        def __set__(self, x):
            global Chunk_totalUpdates
            Chunk_totalUpdates = x

    def __cinit__(self):
        self.__t = tesselator
        self.__dirty = True
        self.__lists = -1
        self.totalUpdates = 0
        self.visible = False
        self.canRender = False

    def __init__(self, Level level, int x0, int y0, int z0,
                 int x1, int y1, int z1, bint fake=False):
        if fake:
            return

        self.__level = level
        self.__x0 = x0
        self.__y0 = y0
        self.__z0 = z0
        self.__x1 = x1
        self.__y1 = y1
        self.__z1 = z1

        self.__x = (x0 + x1) / 2.0
        self.__y = (y0 + y1) / 2.0
        self.__z = (z0 + z1) / 2.0

        self.aabb = AABB(x0, y0, z0, x1, y1, z1)
        self.__lists = gl.glGenLists(3)

    cpdef rebuild(self, layer=None):
        cdef int n, count, x, y, z, tileId
        cdef bint z3
        cdef Tesselator t
        cdef Level l

        n = 1
        if layer is None:
            n = 3

            self.canRender = True
            self.updates += 1

        for i in range(n):
            if layer is None or i:
                layer = i

            t = self.__t
            l = self.__level

            gl.glNewList(self.__lists + layer, gl.GL_COMPILE)
            t.begin()

            count = 0
            z3 = False
            for x in range(self.__x0, self.__x1):
                for y in range(self.__y0, self.__y1):
                    for z in range(self.__z0, self.__z1):
                        tileId = l.getTile(x, y, z)
                        if tileId > 0:
                            z3 |= tiles.tiles[tileId].render(t, l, layer, x, y, z)
                            count += 1

            if z3:
                self.canRender = False

            t.end()
            gl.glEndList()
            if count > 0:
                self.totalUpdates += 1

        if layer == 2:
            self.__dirty = False

    cpdef int render(self, int layer):
        return self.__lists + layer

    def setDirty(self):
        if not self.__dirty:
            getMillis()

        self.__dirty = True

    cpdef bint isDirty(self):
        return self.__dirty

    cpdef float compare(self, player):
        cdef float xd = player.x - self.__x
        cdef float yd = player.y - self.__y
        cdef float zd = player.z - self.__z
        return xd * xd + yd * yd + zd * zd

    def reset(self):
        self.__dirty = True
        for i in range(3):
            gl.glNewList(self.__lists + i, gl.GL_COMPILE)
            gl.glEndList()

    def reset2(self):
        gl.glDeleteLists(self.__lists, 3)
