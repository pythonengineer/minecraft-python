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

        bint[8] __skipRenderPass
        public bint isInFrustum

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
        for i in range(8):
            self.__skipRenderPass[i] = False
        self.isInFrustum = False

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

    cpdef rebuild(self, bint isLit):
        cdef int renderPass, x0, y0, z0, xx, yy, zz, xa, ya, za, x, y, z, tileId, tileId2, tileId3, tileId4, inc
        cdef float m, b, br
        cdef Tile rock, tile

        rock = self.__tiles.rock
        rock.isNormalTile = isLit
        self.updates += 1

        x0 = self.__x0
        y0 = self.__y0
        z0 = self.__z0
        xx = self.__x0 + self.__x1
        yy = self.__y0 + self.__y1
        zz = self.__z0 + self.__z1

        cdef Tesselator t = self.__t
        cdef Level l = self.__level

        for renderPass in range(8):
            self.__skipRenderPass[renderPass] = True

            gl.glNewList(self.__lists + renderPass, gl.GL_COMPILE)
            self.__t.begin()

            xa = 0
            ya = 0
            za = 0
            m = 1.0

            if renderPass == 2 or renderPass == 3:
                m = 0.6
            elif renderPass == 4 or renderPass == 5:
                m = 0.8

            if renderPass == 0:
                m = 0.5
                ya = -1
            elif renderPass == 1:
                ya = 1
            elif renderPass == 2:
                za = -1
            elif renderPass == 3:
                za = 1
            elif renderPass == 4:
                xa = -1
            elif renderPass == 5:
                xa = 1

            for y in range(y0, yy):
                if renderPass != 5 and renderPass != 4:
                    for z in range(z0, zz):
                        x = x0
                        while x < xx:
                            tileId = l.getTile(x, y, z)
                            if renderPass == 6:
                                if tileId > 0 and not rock.lightOpacity[tileId] and not \
                                   rock.isLiquid[tileId] and \
                                   tiles.tiles[tileId].render(t, l, 0, x, y, z):
                                    self.__skipRenderPass[renderPass] = False
                                x += 1
                            elif renderPass == 7:
                                if rock.isLiquid[tileId] and \
                                   tiles.tiles[tileId].render(t, l, 1, x, y, z):
                                    self.__skipRenderPass[renderPass] = False
                                x += 1
                            else:
                                tileId2 = l.getTile(x + xa, y + ya, z + za)
                                if rock.lightOpacity[tileId] and not \
                                   rock.isLiquid[tileId] and not \
                                   rock.opaqueTileLookup[tileId2]:
                                    inc = 0
                                    b = m * l.getBrightness(x + xa, y + ya, z + za)
                                    if isLit:
                                        while x + inc < xx:
                                            inc += 1
                                            tileId3 = l.getTile(x + inc, y, z)
                                            tileId4 = l.getTile(x + inc + xa, y + ya, z + za)
                                            br = m * l.getBrightness(x + inc + xa, y + ya, z + za)
                                            if b != br or tileId3 != tileId or not \
                                               rock.lightOpacity[tileId3] or \
                                               rock.opaqueTileLookup[tileId4]:
                                                break
                                    else:
                                        inc = 1

                                    tile = self.__tiles.tiles[tileId]
                                    t.colorFloat(b, b, b)
                                    tile.renderBlockFromSide(t, x, y, z, renderPass, inc - 1)
                                    self.__skipRenderPass[renderPass] = False
                                    x += inc
                                else:
                                    x += 1
                else:
                    for x in range(x0, xx):
                        z = z0
                        while z < zz:
                            tileId = l.getTile(x, y, z)
                            tileId2 = l.getTile(x + xa, y + ya, z + za)
                            if rock.lightOpacity[tileId] and not \
                               rock.isLiquid[tileId] and not \
                               rock.opaqueTileLookup[tileId2]:
                                b = m * l.getBrightness(x + xa, y + ya, z + za)
                                inc = 0
                                if isLit:
                                    while z + inc < zz:
                                        inc += 1
                                        tileId3 = l.getTile(x, y, z + inc)
                                        tileId4 = l.getTile(x + xa, y + ya, z + inc + za)
                                        br = m * l.getBrightness(x + xa, y + ya, z + inc + za)
                                        if b != br or tileId3 != tileId or not \
                                           rock.lightOpacity[tileId3] or \
                                           rock.opaqueTileLookup[tileId4]:
                                            break
                                else:
                                    inc = 1

                                tile = self.__tiles.tiles[tileId]
                                t.colorFloat(b, b, b)
                                tile.renderBlockFromSide(t, x, y, z, renderPass, inc - 1)
                                self.__skipRenderPass[renderPass] = False
                                z += inc
                            else:
                                z += 1

            self.__t.end()
            gl.glEndList()

        rock.isNormalTile = False

    cpdef float compare(self, player):
        cdef float xd = player.x - self.__x0
        cdef float yd = player.y - self.__y0
        cdef float zd = player.z - self.__z0
        return xd * xd + yd * yd + zd * zd

    cdef __reset(self):
        cdef int renderPass
        for renderPass in range(8):
            self.__skipRenderPass[renderPass] = True

    def clear(self):
        self.__reset()
        self.__level = None

    cpdef render(self, list chunkBuffer, int startingIndex, int renderPass,
                 float x, float y, float z):
        if not self.isInFrustum:
            return startingIndex

        if renderPass == 0:
            if not self.__skipRenderPass[0] and y < self.__y0 + self.__y1 + 0.5:
                chunkBuffer[startingIndex] = self.__lists
                startingIndex += 1
            if not self.__skipRenderPass[1] and y > self.__y0 - 0.5:
                chunkBuffer[startingIndex] = self.__lists + 1
                startingIndex += 1
            if not self.__skipRenderPass[2] and z < self.__z0 + self.__z1 + 0.5:
                chunkBuffer[startingIndex] = self.__lists + 2
                startingIndex += 1
            if not self.__skipRenderPass[3] and z > self.__z0 - 0.5:
                chunkBuffer[startingIndex] = self.__lists + 3
                startingIndex += 1
            if not self.__skipRenderPass[4] and x < self.__x0 + self.__x1 + 0.5:
                chunkBuffer[startingIndex] = self.__lists + 4
                startingIndex += 1
            if not self.__skipRenderPass[5] and x > self.__x0 - 0.5:
                chunkBuffer[startingIndex] = self.__lists + 5
                startingIndex += 1
            if not self.__skipRenderPass[6]:
                chunkBuffer[startingIndex] = self.__lists + 6
                startingIndex += 1
        elif not self.__skipRenderPass[7]:
            chunkBuffer[startingIndex] = self.__lists + 7
            startingIndex += 1

        return startingIndex

    cpdef updateInFrustum(self, Frustum frustum):
        self.isInFrustum = frustum.cubeInFrustum(self.__x0, self.__y0, self.__z0,
                                                 self.__x0 + self.__x1,
                                                 self.__y0 + self.__y1,
                                                 self.__z0 + self.__z1)
