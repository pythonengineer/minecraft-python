# cython: language_level=3

from mc.net.minecraft.renderer.Frustum cimport Frustum
from mc.net.minecraft.renderer.Tesselator cimport Tesselator
from mc.net.minecraft.renderer.Tesselator import tesselator
from mc.net.minecraft.level.tile.Tiles cimport Tiles
from mc.net.minecraft.level.tile.Tiles import tiles
from mc.net.minecraft.level.Level cimport Level
from pyglet import gl

cdef int Chunk_updates = 0

cdef class Chunk:

    cdef:
        Level __level
        Tesselator __t
        Tiles __tiles

        int __lists
        int __x0
        int __y0
        int __z0
        int __x1
        int __y1
        int __z1

        bint[2] __skipRenderPass
        public bint _isInFrustum

    property updates:

        def __get__(self):
            return Chunk_updates

        def __set__(self, x):
            global Chunk_updates
            Chunk_updates = x

    def __cinit__(self):
        self.__tiles = tiles
        self.__t = tesselator
        self.__lists = -1
        self.__skipRenderPass[0] = False
        self.__skipRenderPass[1] = False

    def __init__(self, Level level, int x0, int y0, int z0,
                 int size, int lists, bint fake=False):
        if fake:
            return

        self.__level = level
        self.__x0 = x0
        self.__y0 = y0
        self.__z0 = z0
        self.__x1 = size
        self.__y1 = size
        self.__z1 = size
        self.__lists = lists
        self.__reset()

    cpdef float compare(self, player):
        cdef float xd = player.x - self.__x0
        cdef float yd = player.y - self.__y0
        cdef float zd = player.z - self.__z0
        return xd * xd + yd * yd + zd * zd

    cdef __reset(self):
        cdef int i
        for i in range(2):
            gl.glNewList(self.__lists + i, gl.GL_COMPILE)
            gl.glEndList()

    def clear(self):
        self.__reset()
        self.__level = None

    cpdef rebuild(self):
        cdef int layer, x0, y0, z0, xx, yy, zz, x, y, z, tileId
        cdef bint z3

        self.updates += 1

        cdef Tesselator t = self.__t
        cdef Level l = self.__level

        for layer in range(2):
            x0 = self.__x0
            y0 = self.__y0
            z0 = self.__z0
            xx = self.__x0 + self.__x1
            yy = self.__y0 + self.__y1
            zz = self.__z0 + self.__z1

            gl.glNewList(self.__lists + layer, gl.GL_COMPILE)
            self.__t.begin()

            z3 = False

            for x in range(x0, xx):
                for y in range(y0, yy):
                    for z in range(z0, zz):
                        tileId = self.__level.getTile(x, y, z)
                        if tileId > 0:
                            z3 |= self.__tiles.tiles[tileId].render(t, l, layer, x, y, z)

            self.__t.end()
            gl.glEndList()
            if self.__skipRenderPass[layer] == z3:
                self.__skipRenderPass[layer] = z3

    cpdef render(self, buffer, int layer):
        if self._isInFrustum and not self.__skipRenderPass[layer]:
            buffer.put(self.__lists + layer)

    cpdef isInFrustum(self, Frustum frustum):
        self._isInFrustum = frustum.cubeInFrustum(self.__x0, self.__y0, self.__z0,
                                                  self.__x0 + self.__x1,
                                                  self.__y0 + self.__y1,
                                                  self.__z0 + self.__z1)
