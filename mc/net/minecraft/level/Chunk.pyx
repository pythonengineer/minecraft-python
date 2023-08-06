# cython: language_level=3

from mc.net.minecraft.level.Tesselator cimport Tesselator
from mc.net.minecraft.level.Tesselator import tesselator
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
        public int lists
        public bint dirty
        public object dirtiedTime

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
        self.dirty = True
        self.dirtiedTime = 0
        self.lists = -1

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
        self.lists = gl.glGenLists(2)

    cpdef rebuild(self, layer=None):
        cdef int n, count, x, y, z, tileId
        cdef Tesselator t
        cdef Level l

        n = 1 if layer is not None else 2
        for i in range(n):
            if layer is None or i:
                layer = i

            self.dirty = False
            self.updates += 1

            t = self.__t
            l = self.level

            before = getNs()
            gl.glNewList(self.lists + layer, gl.GL_COMPILE)
            t.init()
            count = 0
            for x in range(self.x0, self.x1):
                for y in range(self.y0, self.y1):
                    for z in range(self.z0, self.z1):
                        tileId = self.level.getTile(x, y, z)
                        if tileId > 0:
                            tiles.tiles[tileId].render(t, l, layer, x, y, z)
                            count += 1
            t.flush()
            gl.glEndList()
            after = getNs()
            if count > 0:
                self.totalTime += after - before
                self.totalUpdates += 1

    cpdef render(self, int layer):
        gl.glCallList(self.lists + layer)

    def setDirty(self):
        if not self.dirty:
            self.dirtiedTime = getMillis()

        self.dirty = True

    cpdef bint isDirty(self):
        return self.dirty

    cpdef float distanceToSqr(self, player):
        cdef float xd = player.x - self.x
        cdef float yd = player.y - self.y
        cdef float zd = player.z - self.z
        return xd * xd + yd * yd + zd * zd
