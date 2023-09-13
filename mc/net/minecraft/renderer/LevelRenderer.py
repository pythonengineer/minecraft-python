from mc.net.minecraft.level.tile.Tile import Tile
from mc.net.minecraft.level.tile.Tiles import tiles
from mc.net.minecraft.renderer.DistanceSorter import DistanceSorter
from mc.net.minecraft.renderer.Tesselator import tesselator
from mc.net.minecraft.renderer.Chunk import Chunk
from mc.CompatibilityShims import BufferUtils, getMillis
from pyglet import gl
from functools import cmp_to_key

import math

class LevelRenderer:
    MAX_REBUILDS_PER_FRAME = 4
    CHUNK_SIZE = 16

    def __init__(self, minecraft, textures):
        self.minecraft = minecraft
        self.textures = textures
        self.level = None
        self.ib = BufferUtils.createIntBuffer(65536)
        self.allDirtyChunks = []
        self.__sortedChunks = []
        self.chunks = []
        self.__chunkBuffer = [0] * 50000
        self.cloudTickCounter = 0
        self.__lX = -9999.0
        self.__lY = -9999.0
        self.__lZ = -9999.0
        self.hurtTime = 0.0
        self.surroundLists = gl.glGenLists(2)
        self.glLists = gl.glGenLists(4096 << 6 << 1)

    def setLevel(self, level):
        if self.level:
            self.level.removeListener(self)

        self.level = level
        if self.level:
            level.addListener(self)
            self.compileSurroundingGround()

    def compileSurroundingGround(self):
        if self.chunks:
            for chunk in self.chunks:
                chunk.clear()

        self.__xChunks = self.level.width // self.CHUNK_SIZE
        self.__yChunks = self.level.depth // self.CHUNK_SIZE
        self.__zChunks = self.level.height // self.CHUNK_SIZE
        self.chunks = [None] * self.__xChunks * self.__yChunks * self.__zChunks
        self.__sortedChunks = [None] * self.__xChunks * self.__yChunks * self.__zChunks

        lists = 0
        for x in range(self.__xChunks):
            for y in range(self.__yChunks):
                for z in range(self.__zChunks):
                    self.chunks[(z * self.__yChunks + y) * self.__xChunks + x] = Chunk(self.level,
                                                                                       x << 4,
                                                                                       y << 4,
                                                                                       z << 4,
                                                                                       LevelRenderer.CHUNK_SIZE,
                                                                                       self.glLists + lists)
                    self.__sortedChunks[(z * self.__yChunks + y) * self.__xChunks + x] = self.chunks[(z * self.__yChunks + y) * self.__xChunks + x]
                    lists += 2

        for chunk in self.allDirtyChunks:
            chunk.dirty = False

        self.allDirtyChunks.clear()
        gl.glNewList(self.surroundLists, gl.GL_COMPILE)
        gl.glColor4f(0.5, 0.5, 0.5, 1.0)
        t = tesselator
        y = self.level.getGroundLevel()
        s = 128
        if s > self.level.width:
            s = self.level.width
        if s > self.level.height:
            s = self.level.height
        d = 2048 // s
        t.begin()
        for xx in range(-s * d, self.level.width + s * d, s):
            for zz in range(-s * d, self.level.height + s * d, s):
                yy = y
                if xx >= 0 and zz >= 0 and xx < self.level.width and zz < self.level.height:
                    yy = 0.0

                t.vertexUV(xx + 0, yy, zz + s, 0.0, s)
                t.vertexUV(xx + s, yy, zz + s, s, s)
                t.vertexUV(xx + s, yy, zz + 0, s, 0.0)
                t.vertexUV(xx + 0, yy, zz + 0, 0.0, 0.0)

        t.end()
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.textures.loadTexture('rock.png'))
        gl.glColor3f(0.8, 0.8, 0.8)
        t.begin()

        for xx in range(0, self.level.width, s):
            t.vertexUV(xx + 0, 0.0, 0.0, 0.0, 0.0)
            t.vertexUV(xx + s, 0.0, 0.0, s, 0.0)
            t.vertexUV(xx + s, y, 0.0, s, y)
            t.vertexUV(xx + 0, y, 0.0, 0.0, y)

            t.vertexUV(xx + 0, y, self.level.height, 0.0, y)
            t.vertexUV(xx + s, y, self.level.height, s, y)
            t.vertexUV(xx + s, 0.0, self.level.height, s, 0.0)
            t.vertexUV(xx + 0, 0.0, self.level.height, 0.0, 0.0)

        gl.glColor3f(0.6, 0.6, 0.6)

        for zz in range(0, self.level.height, s):
            t.vertexUV(0.0, y, zz + 0, 0.0, 0.0)
            t.vertexUV(0.0, y, zz + s, s, 0.0)
            t.vertexUV(0.0, 0.0, zz + s, s, y)
            t.vertexUV(0.0, 0.0, zz + 0, 0.0, y)

            t.vertexUV(self.level.width, 0.0, zz + 0, 0.0, y)
            t.vertexUV(self.level.width, 0.0, zz + s, s, y)
            t.vertexUV(self.level.width, y, zz + s, s, 0.0)
            t.vertexUV(self.level.width, y, zz + 0, 0.0, 0.0)

        t.end()
        gl.glEndList()
        gl.glNewList(self.surroundLists + 1, gl.GL_COMPILE)
        gl.glColor3f(1.0, 1.0, 1.0)
        y = self.level.getWaterLevel()
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        t = tesselator
        s = 128
        if s > self.level.width:
            s = self.level.width
        if s > self.level.height:
            s = self.level.height

        d = 2048 // s
        t.begin()

        for xx in range(-s * d, self.level.width + s * d, s):
            for zz in range(-s * d, self.level.height + s * d, s):
                yy = y - 0.1
                if xx < 0 or zz < 0 or xx >= self.level.width or zz >= self.level.height:
                    t.vertexUV(xx + 0, yy, zz + s, 0.0, s)
                    t.vertexUV(xx + s, yy, zz + s, s, s)
                    t.vertexUV(xx + s, yy, zz + 0, s, 0.0)
                    t.vertexUV(xx + 0, yy, zz + 0, 0.0, 0.0)

                    t.vertexUV(xx + 0, yy, zz + 0, 0.0, 0.0)
                    t.vertexUV(xx + s, yy, zz + 0, s, 0.0)
                    t.vertexUV(xx + s, yy, zz + s, s, s)
                    t.vertexUV(xx + 0, yy, zz + s, 0.0, s)
        t.end()
        gl.glDisable(gl.GL_BLEND)
        gl.glEndList()
        self.setDirty(0, 0, 0, self.level.width, self.level.depth, self.level.height)

    def render(self, player, layer):
        xd = player.x - self.__lX
        yd = player.y - self.__lY
        zd = player.z - self.__lZ
        if xd * xd + yd * yd + zd * zd > 64.0:
            self.__lX = player.x
            self.__lY = player.y
            self.__lZ = player.z
            self.__sortedChunks = sorted(self.__sortedChunks, key=cmp_to_key(DistanceSorter(player).compare))

        startingIndex = 0
        for chunk in self.__sortedChunks:
            startingIndex = chunk.render(self.__chunkBuffer, startingIndex, layer)

        self.ib.clear()
        self.ib.put(self.__chunkBuffer, 0, startingIndex)
        self.ib.flip()
        if self.ib.remaining() > 0:
            gl.glBindTexture(gl.GL_TEXTURE_2D, self.textures.loadTexture('terrain.png'))
            gl.glCallLists(self.ib.capacity(), gl.GL_INT, self.ib)

        return self.ib.remaining()

    def renderClouds(self, partialTicks):
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.textures.loadTexture('clouds.png'))
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        r = (self.level.cloudColor >> 16 & 0xFF) / 255.0
        g = (self.level.cloudColor >> 8 & 0xFF) / 255.0
        b = (self.level.cloudColor & 0xFF) / 255.0
        if self.minecraft.options.anaglyph3d:
            nr = (r * 30.0 + g * 59.0 + b * 11.0) / 100.0
            g = (r * 30.0 + g * 70.0) / 100.0
            b = (r * 30.0 + b * 70.0) / 100.0
            r = nr

        t = tesselator
        f3 = 0.0
        f4 = 4.8828125E-4
        f3 = self.level.depth + 2.
        f1 = (self.cloudTickCounter + partialTicks) * f4 * 0.03
        f5 = 0.0
        t.begin()
        t.colorFloat(r, g, b)

        for i8 in range(-2048, self.level.width + 2048, 512):
            for i6 in range(-2048, self.level.height + 2048, 512):
                t.vertexUV(i8, f3, i6 + 512., i8 * f4 + f1, (i6 + 512.) * f4)
                t.vertexUV(i8 + 512., f3, i6 + 512., (i8 + 512.) * f4 + f1, (i6 + 512.) * f4)
                t.vertexUV(i8 + 512., f3, i6, (i8 + 512.) * f4 + f1, i6 * f4)
                t.vertexUV(i8, f3, i6, i8 * f4 + f1, i6 * f4)
                t.vertexUV(i8, f3, i6, i8 * f4 + f1, i6 * f4)
                t.vertexUV(i8 + 512., f3, i6, (i8 + 512.) * f4 + f1, i6 * f4)
                t.vertexUV(i8 + 512., f3, i6 + 512., (i8 + 512.) * f4 + f1, (i6 + 512.) * f4)
                t.vertexUV(i8, f3, i6 + 512., i8 * f4 + f1, (i6 + 512.) * f4)

        t.end()
        gl.glDisable(gl.GL_TEXTURE_2D)
        t.begin()
        r = (self.level.skyColor >> 16 & 0xFF) / 255.0
        g = (self.level.skyColor >> 8 & 0xFF) / 255.0
        b = (self.level.skyColor & 0xFF) / 255.0
        if self.minecraft.options.anaglyph3d:
            nr = (r * 30.0 + g * 59.0 + b * 11.0) / 100.0
            g = (r * 30.0 + g * 70.0) / 100.0
            b = (r * 30.0 + b * 70.0) / 100.0
            r = nr

        t.colorFloat(r, g, b)
        f3 = self.level.depth + 10.

        for i7 in range(-2048, self.level.width + 2048, 512):
            for i8 in range(-2048, self.level.height + 2048, 512):
                t.vertex(i7, f3, i8)
                t.vertex(i7 + 512., f3, i8)
                t.vertex(i7 + 512., f3, i8 + 512.)
                t.vertex(i7, f3, i8 + 512.)

        t.end()
        gl.glEnable(gl.GL_TEXTURE_2D)

    def renderBasicTile(self, x, y, z):
        tile = self.level.getTile(x, y, z)
        if tile == 0 or not tiles.tiles[tile].isSolid():
            return

        gl.glColor4f(0.2, 0.2, 0.2, 1.0)
        gl.glDepthFunc(gl.GL_LESS)
        t = tesselator
        t.begin()
        for face in range(6):
            tiles.tiles[tile].renderFace(t, x, y, z, face)

        t.end()
        gl.glCullFace(gl.GL_FRONT)
        t.begin()
        for face in range(6):
            tiles.tiles[tile].renderFace(t, x, y, z, face)

        t.end()
        gl.glCullFace(gl.GL_BACK)
        gl.glDepthFunc(gl.GL_LEQUAL)

    def renderHit(self, h, mode, tileType):
        t = tesselator
        gl.glEnable(gl.GL_BLEND)
        gl.glEnable(gl.GL_ALPHA_TEST)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE)
        gl.glColor4f(1.0, 1.0, 1.0, (math.sin(getMillis() / 100.0) * 0.2 + 0.4) * 0.5)
        if self.hurtTime > 0.0:
            gl.glBlendFunc(gl.GL_DST_COLOR, gl.GL_SRC_COLOR)
            id_ = self.textures.loadTexture('terrain.png')
            gl.glBindTexture(gl.GL_TEXTURE_2D, id_)
            gl.glColor4f(1.0, 1.0, 1.0, 0.5)
            gl.glPushMatrix()
            tile = self.level.getTile(h.x, h.y, h.z)
            tile = tiles.tiles[tile] if tile > 0 else None
            x = (tile.xx0 + tile.xx1) / 2.0
            y = (tile.yy0 + tile.yy1) / 2.0
            z = (tile.zz0 + tile.zz1) / 2.0
            gl.glTranslatef(h.x + x, h.y + y, h.z + z)
            gl.glScalef(1.01, 1.01, 1.01)
            gl.glTranslatef(-(h.x + x), -(h.y + y), -(h.z + z))
            t.begin()
            t.noColor()
            gl.glDepthMask(False)
            if not tile:
                tile = tiles.rock

            for face in range(6):
                tile.renderFaceNoTexture(t, h.x, h.y, h.z,
                                         face, 240 + int(self.hurtTime * 10.0))
            t.end()
            gl.glDepthMask(True)
            gl.glPopMatrix()

        gl.glDisable(gl.GL_BLEND)
        gl.glDisable(gl.GL_ALPHA_TEST)

    def setDirty(self, x0, y0, z0, x1, y1, z1):
        x0 //= self.CHUNK_SIZE
        x1 //= self.CHUNK_SIZE
        y0 //= self.CHUNK_SIZE
        y1 //= self.CHUNK_SIZE
        z0 //= self.CHUNK_SIZE
        z1 //= self.CHUNK_SIZE

        if x0 < 0: x0 = 0
        if y0 < 0: y0 = 0
        if z0 < 0: z0 = 0
        if x1 >= self.__xChunks: x1 = self.__xChunks - 1
        if y1 >= self.__yChunks: y1 = self.__yChunks - 1
        if z1 >= self.__zChunks: z1 = self.__zChunks - 1

        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                for z in range(z0, z1 + 1):
                    chunk = self.chunks[(z * self.__yChunks + y) * self.__xChunks + x]
                    if not chunk.dirty:
                        chunk.dirty = True
                        self.allDirtyChunks.append(chunk)
