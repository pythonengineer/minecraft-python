# cython: language_level=3

from mc.net.minecraft.renderer.Tesselator cimport Tesselator
from mc.net.minecraft.renderer.Tesselator import tesselator
from mc.net.minecraft.level.Level cimport Level
from mc.net.minecraft.level.tile.Tiles import tiles
from mc.net.minecraft.phys.AABB import AABB
from mc.CompatibilityShims import getMillis, getNs
from pyglet import gl

cdef int Chunk_updates = 0
cdef object Chunk_totalTime = 0
cdef int Chunk_totalUpdates = 0

cdef class Chunk:

    cdef:
        public Level level
        Tesselator __t

        public int x0
        public int y0
        public int z0
        public int x1
        public int y1
        public int z1

        public float x
        public float y
        public float z

        public object aabb
        int __lists
        bint __dirty
        public object dirtiedTime
        public bint visible

    property updates:

        def __get__(self):
            return Chunk_updates

        def __set__(self, x):
            global Chunk_updates
            Chunk_updates = x

    property totalTime:

        def __get__(self):
            return Chunk_totalTime

        def __set__(self, x):
            global Chunk_totalTime
            Chunk_totalTime = x

    property totalUpdates:

        def __get__(self):
            return Chunk_totalUpdates

        def __set__(self, x):
            global Chunk_totalUpdates
            Chunk_totalUpdates = x

    def __cinit__(self):
        self.__t = tesselator
        self.__dirty = True
        self.dirtiedTime = 0
        self.__lists = -1
        self.totalTime = 0
        self.totalUpdates = 0
        self.visible = False

    def __init__(self, Level level, int x0, int y0, int z0,
                 int x1, int y1, int z1, bint fake=False):
        if fake:
            return

        self.level = level
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1

        self.x = (x0 + x1) / 2.0
        self.y = (y0 + y1) / 2.0
        self.z = (z0 + z1) / 2.0

        self.aabb = AABB(x0, y0, z0, x1, y1, z1)
        self.__lists = gl.glGenLists(3)

    cpdef rebuild(self, layer=None):
        cdef int n, count, x, y, z, tileId
        cdef Tesselator t
        cdef Level l

        n = 1
        if layer is None:
            n = 3

            self.updates += 1

        for i in range(n):
            if layer is None or i:
                layer = i

            t = self.__t
            l = self.level

            before = getNs()
            gl.glNewList(self.__lists + layer, gl.GL_COMPILE)
            t.begin()
            count = 0
            for x in range(self.x0, self.x1):
                for y in range(self.y0, self.y1):
                    for z in range(self.z0, self.z1):
                        tileId = self.level.getTile(x, y, z)
                        if tileId > 0:
                            tiles.tiles[tileId].render(t, l, layer, x, y, z)
                            count += 1
            t.end()
            gl.glEndList()
            after = getNs()
            if count > 0:
                self.totalTime += after - before
                self.totalUpdates += 1

        if layer == 2:
            self.__dirty = False

    cpdef render(self, int layer):
        gl.glCallList(self.__lists + layer)

    def setDirty(self):
        if not self.__dirty:
            self.dirtiedTime = getMillis()

        self.__dirty = True

    cpdef bint isDirty(self):
        return self.__dirty

    cpdef float distanceToSqr(self, player):
        cdef float xd = player.x - self.x
        cdef float yd = player.y - self.y
        cdef float zd = player.z - self.z
        return xd * xd + yd * yd + zd * zd

    def reset(self):
        self.__dirty = True
        for i in range(3):
            gl.glNewList(self.__lists + i, gl.GL_COMPILE)
            gl.glEndList()
