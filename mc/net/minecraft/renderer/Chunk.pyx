# cython: language_level=3

from mc.net.minecraft.renderer.Frustum cimport Frustum
from mc.net.minecraft.renderer.Tesselator cimport Tesselator
from mc.net.minecraft.renderer.Tesselator import tesselator
from mc.net.minecraft.level.tile.Tiles cimport Tiles
from mc.net.minecraft.level.tile.Tiles import tiles
from mc.net.minecraft.level.tile.Tile cimport Tile
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
        public bint isInFrustum
        public bint dirty

    @property
    def updates(self):
        return Chunk_updates

    @updates.setter
    def updates(self, x):
        global Chunk_updates
        Chunk_updates = x

    def __cinit__(self):
        self.__tiles = tiles
        self.__t = tesselator
        self.__lists = -1
        for i in range(2):
            self.__skipRenderPass[i] = False
        self.isInFrustum = False
        self.dirty = False

    def __init__(self, Level level, int x0, int y0, int z0,
                 int size, int lists, bint fake=False):
        if fake:
            return

        self.__level = level
        self.__x0 = x0
        self.__y0 = y0
        self.__z0 = z0
        self.__x1 = 16
        self.__y1 = 16
        self.__z1 = 16
        self.__lists = lists
        self.__reset()

    cpdef rebuild(self):
        cdef int layer, x0, y0, z0, xx, yy, zz, x, y, z
        cdef int tileId
        cdef bint z8, z9
        cdef Tile tile

        rock = self.__tiles.rock
        self.updates += 1

        x0 = self.__x0
        y0 = self.__y0
        z0 = self.__z0
        xx = self.__x0 + self.__x1
        yy = self.__y0 + self.__y1
        zz = self.__z0 + self.__z1

        cdef Tesselator t = self.__t
        cdef Level l = self.__level

        for layer in range(2):
            self.__skipRenderPass[layer] = True

        for layer in range(2):
            z8 = False
            z9 = False

            gl.glNewList(self.__lists + layer, gl.GL_COMPILE)
            self.__t.begin()

            for x in range(x0, xx):
                for y in range(y0, yy):
                    for z in range(z0, zz):
                        tileId = self.__level.getTile(x, y, z)
                        if tileId > 0:
                            tile = self.__tiles.tiles[tileId]
                            if tile.getRenderLayer() != layer:
                                z8 = True
                            else:
                                z9 |= tile.renderFull(self.__level, x, y, z, t)

            self.__t.end()
            gl.glEndList()

            if z9:
                self.__skipRenderPass[layer] = False

            if not z8:
                break

    cpdef float compare(self, player):
        cdef float xd = player.x - self.__x0
        cdef float yd = player.y - self.__y0
        cdef float zd = player.z - self.__z0
        return xd * xd + yd * yd + zd * zd

    cdef __reset(self):
        cdef int layer
        for layer in range(2):
            self.__skipRenderPass[layer] = True

    def clear(self):
        self.__reset()
        self.__level = None

    cpdef render(self, list chunkBuffer, int startingIndex, int renderPass):
        if not self.isInFrustum:
            return startingIndex

        if not self.__skipRenderPass[renderPass]:
            chunkBuffer[startingIndex] = self.__lists + renderPass
            startingIndex += 1

        return startingIndex

    cpdef updateInFrustum(self, Frustum frustum):
        self.isInFrustum = frustum.cubeInFrustum(self.__x0, self.__y0, self.__z0,
                                                 self.__x0 + self.__x1,
                                                 self.__y0 + self.__y1,
                                                 self.__z0 + self.__z1)
