from mc.net.minecraft.level.DistanceSorter import DistanceSorter
from mc.net.minecraft.level.Chunk import Chunk
from mc.net.minecraft.level.tile.Tile import Tile
from mc.net.minecraft.level.tile.Tiles import tiles
from mc.net.minecraft.renderer.Tesselator import tesselator
from mc.CompatibilityShims import BufferUtils, getMillis
from pyglet import gl
from functools import cmp_to_key

import math

class LevelRenderer:
    MAX_REBUILDS_PER_FRAME = 4
    CHUNK_SIZE = 16
    chunks = []
    drawDistance = 0
    __dummyBuffer = BufferUtils.createIntBuffer(1024)

    def __init__(self, level, textures):
        self.level = level
        self.__textures = textures
        level.levelListeners.add(self)
        self.surroundLists = gl.glGenLists(2)
        self.allChanged()

    def allChanged(self):
        self.__lX = -900000.0
        self.__lY = -900000.0
        self.__lZ = -900000.0
        if self.chunks:
            for chunk in self.chunks:
                chunk.reset2()

        self.__xChunks = (self.level.width + self.CHUNK_SIZE - 1) // self.CHUNK_SIZE
        self.__yChunks = (self.level.depth + self.CHUNK_SIZE - 1) // self.CHUNK_SIZE
        self.__zChunks = (self.level.height + self.CHUNK_SIZE - 1) // self.CHUNK_SIZE
        self.chunks = [None] * self.__xChunks * self.__yChunks * self.__zChunks
        self.__sortedChunks = [None] * self.__xChunks * self.__yChunks * self.__zChunks
        for x in range(self.__xChunks):
            for y in range(self.__yChunks):
                for z in range(self.__zChunks):
                    x0 = x * self.CHUNK_SIZE
                    y0 = y * self.CHUNK_SIZE
                    z0 = z * self.CHUNK_SIZE
                    x1 = (x + 1) * self.CHUNK_SIZE
                    y1 = (y + 1) * self.CHUNK_SIZE
                    z1 = (z + 1) * self.CHUNK_SIZE

                    if x1 > self.level.width: x1 = self.level.width
                    if y1 > self.level.depth: y1 = self.level.depth
                    if z1 > self.level.height: z1 = self.level.height
                    self.chunks[(x + y * self.__xChunks) * self.__zChunks + z] = Chunk(self.level, x0, y0, z0, x1, y1, z1)
                    self.__sortedChunks[(x + y * self.__xChunks) * self.__zChunks + z] = self.chunks[(x + y * self.__xChunks) * self.__zChunks + z]

        gl.glNewList(self.surroundLists + 0, gl.GL_COMPILE)
        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.__textures.loadTexture('rock.png', gl.GL_NEAREST))
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        t = tesselator
        y = 32.0 - 2.0
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
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.__textures.loadTexture('rock.png', gl.GL_NEAREST))
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
        gl.glDisable(gl.GL_BLEND)
        gl.glDisable(gl.GL_TEXTURE_2D)
        gl.glEndList()
        gl.glNewList(self.surroundLists + 1, gl.GL_COMPILE)
        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glColor3f(1.0, 1.0, 1.0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.__textures.loadTexture('water.png', gl.GL_NEAREST))
        y = 32.0
        gl.glEnable(gl.GL_BLEND)
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
        gl.glDisable(gl.GL_TEXTURE_2D)
        gl.glEndList()

        for chunk in self.chunks:
            chunk.reset()

    def render(self, player, layer):
        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.__textures.loadTexture('terrain.png', gl.GL_NEAREST))

        xd = player.x - self.__lX
        yd = player.y - self.__lY
        zd = player.z - self.__lZ
        if xd * xd + yd * yd + zd * zd > 64.0:
            self.__lX = player.x
            self.__lY = player.y
            self.__lZ = player.z
            self.__sortedChunks = sorted(self.__sortedChunks, key=cmp_to_key(DistanceSorter(player).compare))

        self.__dummyBuffer.clear()

        for chunk in self.__sortedChunks:
            if chunk.visible and not chunk.canRender:
                dd = 256 / (1 << self.drawDistance)
                if self.drawDistance == 0 or chunk.compare(player) < dd * dd:
                    i7 = chunk.render(layer)
                    self.__dummyBuffer.put(i7)
                    if self.__dummyBuffer.remaining() == 0:
                        self.__dummyBuffer.flip()
                        gl.glCallLists(self.__dummyBuffer.capacity(), gl.GL_INT, self.__dummyBuffer)
                        self.__dummyBuffer.clear()

        if self.__dummyBuffer.position() > 0:
            self.__dummyBuffer.flip()
            gl.glCallLists(self.__dummyBuffer.capacity(), gl.GL_INT, self.__dummyBuffer)

        gl.glDisable(gl.GL_TEXTURE_2D)

    def renderHit(self, player, h, mode, tileType):
        t = tesselator
        gl.glEnable(gl.GL_BLEND)
        gl.glEnable(gl.GL_ALPHA_TEST)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE)
        gl.glColor4f(1.0, 1.0, 1.0, (math.sin(getMillis() / 100.0) * 0.2 + 0.4) * 0.5)
        if mode == 0:
            t.begin()
            for i in range(6):
                tiles.rock.renderFaceNoTexture(player, t, h.x, h.y, h.z, i)
            t.end()
        else:
            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
            br = math.sin(getMillis() / 100.0) * 0.2 + 0.8
            gl.glColor4f(br, br, br, math.sin(getMillis() / 200.0) * 0.2 + 0.5)
            gl.glEnable(gl.GL_TEXTURE_2D)
            id_ = self.__textures.loadTexture('terrain.png', gl.GL_NEAREST)
            gl.glBindTexture(gl.GL_TEXTURE_2D, id_)
            x = h.x
            y = h.y
            z = h.z
            if h.f == 0: y -= 1
            elif h.f == 1: y += 1
            elif h.f == 2: z -= 1
            elif h.f == 3: z += 1
            elif h.f == 4: x -= 1
            elif h.f == 5: x += 1
            t.begin()
            t.noColor()
            tiles.tiles[tileType].render(t, self.level, 0, x, y, z)
            tiles.tiles[tileType].render(t, self.level, 1, x, y, z)
            t.end()
            gl.glDisable(gl.GL_TEXTURE_2D)
        gl.glDisable(gl.GL_BLEND)
        gl.glDisable(gl.GL_ALPHA_TEST)

    @staticmethod
    def renderHitOutline(h, mode):
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glColor4f(0.0, 0.0, 0.0, 0.4)
        x = h.x
        y = h.y
        z = h.z
        if mode == 1:
            if h.f == 0: y -= 1.0
            elif h.f == 1: y += 1.0
            elif h.f == 2: z -= 1.0
            elif h.f == 3: z += 1.0
            elif h.f == 4: x -= 1.0
            elif h.f == 5: x += 1.0
        gl.glBegin(gl.GL_LINE_STRIP)
        gl.glVertex3f(x, y, z)
        gl.glVertex3f(x + 1.0, y, z)
        gl.glVertex3f(x + 1.0, y, z + 1.0)
        gl.glVertex3f(x, y, z + 1.0)
        gl.glVertex3f(x, y, z)
        gl.glEnd()
        gl.glBegin(gl.GL_LINE_STRIP)
        gl.glVertex3f(x, y + 1.0, z)
        gl.glVertex3f(x + 1.0, y + 1.0, z)
        gl.glVertex3f(x + 1.0, y + 1.0, z + 1.0)
        gl.glVertex3f(x, y + 1.0, z + 1.0)
        gl.glVertex3f(x, y + 1.0, z)
        gl.glEnd()
        gl.glBegin(gl.GL_LINES)
        gl.glVertex3f(x, y, z)
        gl.glVertex3f(x, y + 1.0, z)
        gl.glVertex3f(x + 1.0, y, z)
        gl.glVertex3f(x + 1.0, y + 1.0, z)
        gl.glVertex3f(x + 1.0, y, z + 1.0)
        gl.glVertex3f(x + 1.0, y + 1.0, z + 1.0)
        gl.glVertex3f(x, y, z + 1.0)
        gl.glVertex3f(x, y + 1.0, z + 1.0)
        gl.glEnd()
        gl.glDisable(gl.GL_BLEND)

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
                    self.chunks[(x + y * self.__xChunks) * self.__zChunks + z].setDirty()
