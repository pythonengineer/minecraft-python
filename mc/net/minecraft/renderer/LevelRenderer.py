from mc.net.minecraft.level.tile.Tile import Tile
from mc.net.minecraft.level.tile.Tiles import tiles
from mc.net.minecraft.renderer.DistanceSorter import DistanceSorter
from mc.net.minecraft.renderer.Tesselator import Tesselator, tesselator
from mc.net.minecraft.renderer.Chunk import Chunk
from mc.CompatibilityShims import BufferUtils, getMillis
from pyglet import gl
from functools import cmp_to_key

import math

class LevelRenderer:
    MAX_REBUILDS_PER_FRAME = 4
    CHUNK_SIZE = 16
    level = None
    drawDistance = 0
    dummyBuffer = BufferUtils.createIntBuffer(65536)
    dirtyChunks = set()
    sortedChunks = []
    cloudTickCounter = 0
    __lX = -9999.0
    __lY = -9999.0
    __lZ = -9999.0

    def __init__(self, textures):
        self.textures = textures
        self.surroundLists = gl.glGenLists(2)
        self.__chunkRenderLists = gl.glGenLists(Tesselator.MAX_FLOATS)

    def setLevel(self, level):
        if self.level:
            self.level.removeListener(self)

        self.level = level
        if self.level:
            level.addListener(self)
            self.dummyBuffer = BufferUtils.createIntBuffer(65536)
            self.compileSurroundingGround()

    def compileSurroundingGround(self):
        if self.sortedChunks:
            for chunk in self.sortedChunks:
                chunk.clear()

        self.__xChunks = self.level.width // self.CHUNK_SIZE
        self.__yChunks = self.level.depth // self.CHUNK_SIZE
        self.__zChunks = self.level.height // self.CHUNK_SIZE
        self.sortedChunks = [None] * self.__xChunks * self.__yChunks * self.__zChunks
        self.__chunks = [None] * self.__xChunks * self.__yChunks * self.__zChunks

        lists = 0
        for x in range(self.__xChunks):
            for y in range(self.__yChunks):
                for z in range(self.__zChunks):
                    self.sortedChunks[(z * self.__yChunks + y) * self.__xChunks + x] = Chunk(self.level,
                                                                                             x << 4,
                                                                                             y << 4,
                                                                                             z << 4,
                                                                                             self.CHUNK_SIZE,
                                                                                             self.__chunkRenderLists + lists)
                    self.__chunks[(z * self.__yChunks + y) * self.__xChunks + x] = self.sortedChunks[(z * self.__yChunks + y) * self.__xChunks + x]
                    lists += 2

        self.dirtyChunks.clear()
        gl.glNewList(self.surroundLists, gl.GL_COMPILE)
        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.textures.getTextureId('rock.png'))
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
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.textures.getTextureId('rock.png'))
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
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.textures.getTextureId('water.png'))
        y = self.level.getWaterLevel()
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
        self.setDirty(0, 0, 0, self.level.width, self.level.depth, self.level.height)

    def renderEntities(self, frustum, a):
        for entity in self.level.entities:
            if frustum.isVisible(entity.bb):
                entity.render(self.textures, a)

    def render(self, player, layer, z=None):
        if z is not None:
            x = player
            y = layer
            i6 = self.level.getTile(x, y, z)
            if i6 != 0 and tiles.tiles[i6].isSolid():
                gl.glEnable(gl.GL_TEXTURE_2D)
                gl.glColor4f(0.2, 0.2, 0.2, 1.0)
                gl.glDepthFunc(gl.GL_LESS)
                t = tesselator
                t.begin()

                for i in range(6):
                    tiles.tiles[i6].renderFace(t, x, y, z, i)

                t.end()
                gl.glCullFace(gl.GL_FRONT)
                t.begin()

                for i in range(6):
                    tiles.tiles[i6].renderFace(t, x, y, z, i)

                t.end()
                gl.glCullFace(gl.GL_BACK)
                gl.glDisable(gl.GL_TEXTURE_2D)
                gl.glDepthFunc(gl.GL_LEQUAL)

            return

        xd = player.x - self.__lX
        yd = player.y - self.__lY
        zd = player.z - self.__lZ
        if xd * xd + yd * yd + zd * zd > 64.0:
            self.__lX = player.x
            self.__lY = player.y
            self.__lZ = player.z
            self.__chunks = sorted(self.__chunks, key=cmp_to_key(DistanceSorter(player).compare))

        self.dummyBuffer.clear()

        for chunk in self.__chunks:
            chunk.render(self.dummyBuffer, layer)

        self.dummyBuffer.flip()
        if self.dummyBuffer.remaining() > 0:
            gl.glEnable(gl.GL_TEXTURE_2D)
            gl.glBindTexture(gl.GL_TEXTURE_2D, self.textures.getTextureId('terrain.png'))
            gl.glCallLists(self.dummyBuffer.capacity(), gl.GL_INT, self.dummyBuffer)
            gl.glDisable(gl.GL_TEXTURE_2D)

        return self.dummyBuffer.remaining()

    def renderClouds(self, a):
        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.textures.getTextureId('clouds.png'))
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        t = tesselator
        f3 = 0.0
        f4 = 4.8828125E-4
        f3 = self.level.depth + 2.
        f1 = (self.cloudTickCounter + a) * f4 * 0.03
        f5 = 0.0
        t.begin()

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
        t.colorFloat(0.5, 0.8, 1.0)
        f3 = self.level.depth + 10.

        for i7 in range(-2048, self.level.width + 2048, 512):
            for i8 in range(-2048, self.level.height + 2048, 512):
                t.vertex(i7, f3, i8)
                t.vertex(i7 + 512., f3, i8)
                t.vertex(i7 + 512., f3, i8 + 512.)
                t.vertex(i7, f3, i8 + 512.)

        t.end()

    def renderHit(self, player, h, mode, tileType):
        t = tesselator
        gl.glEnable(gl.GL_BLEND)
        gl.glEnable(gl.GL_ALPHA_TEST)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE)
        gl.glColor4f(1.0, 1.0, 1.0, (math.sin(getMillis() / 100.0) * 0.2 + 0.4) * 0.5)
        if mode == 0:
            t.begin()
            for i in range(6):
                Tile.renderFaceNoTexture(player, t, h.x, h.y, h.z, i)
            t.end()
        else:
            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
            br = math.sin(getMillis() / 100.0) * 0.2 + 0.8
            gl.glColor4f(br, br, br, math.sin(getMillis() / 200.0) * 0.2 + 0.5)
            gl.glEnable(gl.GL_TEXTURE_2D)
            id_ = self.textures.getTextureId('terrain.png')
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
                    self.dirtyChunks.add(self.sortedChunks[(z * self.__yChunks + y) * self.__xChunks + x])
