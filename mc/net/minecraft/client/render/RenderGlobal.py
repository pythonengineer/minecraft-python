from mc.net.minecraft.game.level.block.Blocks import blocks
from mc.net.minecraft.client.render.EntitySorter import EntitySorter
from mc.net.minecraft.client.render.Tessellator import tessellator
from mc.net.minecraft.client.render.WorldRenderer import WorldRenderer
from mc.net.minecraft.client.render.RenderManager import RenderManager
from mc.CompatibilityShims import BufferUtils, getMillis
from pyglet import gl
from functools import cmp_to_key

import math

class RenderGlobal:
    MAX_REBUILDS_PER_FRAME = 3
    CHUNK_SIZE = 16

    def __init__(self, minecraft, renderEngine):
        self.mc = minecraft
        self.renderEngine = renderEngine
        self.worldObj = None
        self.renderIntBuffer = BufferUtils.createIntBuffer(65536)
        self.worldRenderersToUpdate = []
        self.__sortedWorldRenderers = []
        self.worldRenderers = []
        self.globalRenderBlocks = None
        self.renderManager = RenderManager()
        self.__chunkBuffer = [0] * 50000
        self.cloudOffsetX = 0
        self.__prevSortX = -9999.0
        self.__prevSortY = -9999.0
        self.__prevSortZ = -9999.0
        self.damagePartialTime = 0.0
        self.glGenList = gl.glGenLists(2)
        self.__glRenderListBase = gl.glGenLists(4096 << 6 << 1)

    def loadRenderers(self):
        if self.worldRenderers:
            for chunk in self.worldRenderers:
                chunk.stopRendering()

        self.__renderChunksWide = self.worldObj.width // self.CHUNK_SIZE
        self.__renderChunksTall = self.worldObj.height // self.CHUNK_SIZE
        self.__renderChunksDeep = self.worldObj.length // self.CHUNK_SIZE
        self.worldRenderers = [None] * self.__renderChunksWide * self.__renderChunksTall * self.__renderChunksDeep
        self.__sortedWorldRenderers = [None] * self.__renderChunksWide * self.__renderChunksTall * self.__renderChunksDeep

        lists = 0
        for x in range(self.__renderChunksWide):
            for y in range(self.__renderChunksTall):
                for z in range(self.__renderChunksDeep):
                    i = (z * self.__renderChunksTall + y) * self.__renderChunksWide + x
                    self.worldRenderers[i] = WorldRenderer(self.worldObj, x << 4, y << 4,
                                                           z << 4, RenderGlobal.CHUNK_SIZE,
                                                           self.__glRenderListBase + lists)
                    self.__sortedWorldRenderers[i] = self.worldRenderers[i]
                    lists += 2

        for chunk in self.worldRenderersToUpdate:
            chunk.needsUpdate = False

        self.worldRenderersToUpdate.clear()
        gl.glNewList(self.glGenList, gl.GL_COMPILE)
        gl.glColor4f(0.5, 0.5, 0.5, 1.0)
        t = tessellator
        y = self.worldObj.getGroundLevel()
        s = 128
        if s > self.worldObj.width:
            s = self.worldObj.width
        if s > self.worldObj.length:
            s = self.worldObj.length
        d = 2048 // s
        t.startDrawingQuads()
        for xx in range(-s * d, self.worldObj.width + s * d, s):
            for zz in range(-s * d, self.worldObj.length + s * d, s):
                yy = y
                if xx >= 0 and zz >= 0 and xx < self.worldObj.width and zz < self.worldObj.length:
                    yy = 0.0

                t.addVertexWithUV(xx + 0, yy, zz + s, 0.0, s)
                t.addVertexWithUV(xx + s, yy, zz + s, s, s)
                t.addVertexWithUV(xx + s, yy, zz + 0, s, 0.0)
                t.addVertexWithUV(xx + 0, yy, zz + 0, 0.0, 0.0)

        t.draw()
        gl.glColor3f(0.8, 0.8, 0.8)
        t.startDrawingQuads()

        for xx in range(0, self.worldObj.width, s):
            t.addVertexWithUV(xx + 0, 0.0, 0.0, 0.0, 0.0)
            t.addVertexWithUV(xx + s, 0.0, 0.0, s, 0.0)
            t.addVertexWithUV(xx + s, y, 0.0, s, y)
            t.addVertexWithUV(xx + 0, y, 0.0, 0.0, y)

            t.addVertexWithUV(xx + 0, y, self.worldObj.length, 0.0, y)
            t.addVertexWithUV(xx + s, y, self.worldObj.length, s, y)
            t.addVertexWithUV(xx + s, 0.0, self.worldObj.length, s, 0.0)
            t.addVertexWithUV(xx + 0, 0.0, self.worldObj.length, 0.0, 0.0)

        gl.glColor3f(0.6, 0.6, 0.6)

        for zz in range(0, self.worldObj.length, s):
            t.addVertexWithUV(0.0, y, zz + 0, 0.0, 0.0)
            t.addVertexWithUV(0.0, y, zz + s, s, 0.0)
            t.addVertexWithUV(0.0, 0.0, zz + s, s, y)
            t.addVertexWithUV(0.0, 0.0, zz + 0, 0.0, y)

            t.addVertexWithUV(self.worldObj.width, 0.0, zz + 0, 0.0, y)
            t.addVertexWithUV(self.worldObj.width, 0.0, zz + s, s, y)
            t.addVertexWithUV(self.worldObj.width, y, zz + s, s, 0.0)
            t.addVertexWithUV(self.worldObj.width, y, zz + 0, 0.0, 0.0)

        t.draw()
        gl.glEndList()
        gl.glNewList(self.glGenList + 1, gl.GL_COMPILE)
        gl.glColor3f(1.0, 1.0, 1.0)
        y = self.worldObj.rgetGroundLevel()
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        t = tessellator
        s = 128
        if s > self.worldObj.width:
            s = self.worldObj.width
        if s > self.worldObj.length:
            s = self.worldObj.length

        d = 2048 // s
        t.startDrawingQuads()

        for xx in range(-s * d, self.worldObj.width + s * d, s):
            for zz in range(-s * d, self.worldObj.length + s * d, s):
                yy = y - 0.1
                if xx < 0 or zz < 0 or xx >= self.worldObj.width or zz >= self.worldObj.length:
                    t.addVertexWithUV(xx + 0, yy, zz + s, 0.0, s)
                    t.addVertexWithUV(xx + s, yy, zz + s, s, s)
                    t.addVertexWithUV(xx + s, yy, zz + 0, s, 0.0)
                    t.addVertexWithUV(xx + 0, yy, zz + 0, 0.0, 0.0)

                    t.addVertexWithUV(xx + 0, yy, zz + 0, 0.0, 0.0)
                    t.addVertexWithUV(xx + s, yy, zz + 0, s, 0.0)
                    t.addVertexWithUV(xx + s, yy, zz + s, s, s)
                    t.addVertexWithUV(xx + 0, yy, zz + s, 0.0, s)
        t.draw()
        gl.glDisable(gl.GL_BLEND)
        gl.glEndList()
        self.markBlocksForUpdate(0, 0, 0, self.worldObj.width, self.worldObj.height, self.worldObj.length)

    def sortAndRender(self, player, layer):
        xd = player.posX - self.__prevSortX
        yd = player.posY - self.__prevSortY
        zd = player.posZ - self.__prevSortZ
        if xd * xd + yd * yd + zd * zd > 64.0:
            self.__prevSortX = player.posX
            self.__prevSortY = player.posY
            self.__prevSortZ = player.posZ
            self.__sortedWorldRenderers = sorted(
                self.__sortedWorldRenderers,
                key=cmp_to_key(EntitySorter(player).compare)
            )

        startingIndex = 0
        for chunk in self.__sortedWorldRenderers:
            startingIndex = chunk.getGLCallListForPass(self.__chunkBuffer, startingIndex, layer)

        self.renderIntBuffer.clear()
        self.renderIntBuffer.putOffset(self.__chunkBuffer, 0, startingIndex)
        self.renderIntBuffer.flip()
        if self.renderIntBuffer.remaining() > 0:
            gl.glBindTexture(gl.GL_TEXTURE_2D, self.renderEngine.getTexture('terrain.png'))
            self.renderIntBuffer.glCallLists(self.renderIntBuffer.capacity(), gl.GL_INT)

        return self.renderIntBuffer.remaining()

    def renderClouds(self, partialTicks):
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.renderEngine.getTexture('clouds.png'))
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        r = (self.worldObj.cloudColor >> 16 & 0xFF) / 255.0
        g = (self.worldObj.cloudColor >> 8 & 0xFF) / 255.0
        b = (self.worldObj.cloudColor & 0xFF) / 255.0
        if self.mc.options.anaglyph:
            nr = (r * 30.0 + g * 59.0 + b * 11.0) / 100.0
            g = (r * 30.0 + g * 70.0) / 100.0
            b = (r * 30.0 + b * 70.0) / 100.0
            r = nr

        t = tessellator
        f3 = 0.0
        f4 = 0.5 / 1024
        f3 = self.worldObj.height + 2.
        f1 = (self.cloudOffsetX + partialTicks) * f4 * 0.03
        f5 = 0.0
        t.startDrawingQuads()
        t.setColorOpaque_F(r, g, b)

        for i8 in range(-2048, self.worldObj.width + 2048, 512):
            for i6 in range(-2048, self.worldObj.height + 2048, 512):
                t.addVertexWithUV(i8, f3, i6 + 512., i8 * f4 + f1, (i6 + 512.) * f4)
                t.addVertexWithUV(i8 + 512., f3, i6 + 512., (i8 + 512.) * f4 + f1, (i6 + 512.) * f4)
                t.addVertexWithUV(i8 + 512., f3, i6, (i8 + 512.) * f4 + f1, i6 * f4)
                t.addVertexWithUV(i8, f3, i6, i8 * f4 + f1, i6 * f4)
                t.addVertexWithUV(i8, f3, i6, i8 * f4 + f1, i6 * f4)
                t.addVertexWithUV(i8 + 512., f3, i6, (i8 + 512.) * f4 + f1, i6 * f4)
                t.addVertexWithUV(i8 + 512., f3, i6 + 512., (i8 + 512.) * f4 + f1, (i6 + 512.) * f4)
                t.addVertexWithUV(i8, f3, i6 + 512., i8 * f4 + f1, (i6 + 512.) * f4)

        t.draw()
        gl.glDisable(gl.GL_TEXTURE_2D)
        t.startDrawingQuads()
        r = (self.worldObj.skyColor >> 16 & 0xFF) / 255.0
        g = (self.worldObj.skyColor >> 8 & 0xFF) / 255.0
        b = (self.worldObj.skyColor & 0xFF) / 255.0
        if self.mc.options.anaglyph:
            nr = (r * 30.0 + g * 59.0 + b * 11.0) / 100.0
            g = (r * 30.0 + g * 70.0) / 100.0
            b = (r * 30.0 + b * 70.0) / 100.0
            r = nr

        t.setColorOpaque_F(r, g, b)
        f3 = self.worldObj.height + 10.

        for i7 in range(-2048, self.worldObj.width + 2048, 512):
            for i8 in range(-2048, self.worldObj.height + 2048, 512):
                t.addVertex(i7, f3, i8)
                t.addVertex(i7 + 512., f3, i8)
                t.addVertex(i7 + 512., f3, i8 + 512.)
                t.addVertex(i7, f3, i8 + 512.)

        t.draw()
        gl.glEnable(gl.GL_TEXTURE_2D)

    def renderHit(self, h):
        t = tessellator
        gl.glEnable(gl.GL_BLEND)
        gl.glEnable(gl.GL_ALPHA_TEST)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE)
        gl.glColor4f(1.0, 1.0, 1.0, (math.sin(getMillis() / 100.0) * 0.2 + 0.4) * 0.5)
        if self.damagePartialTime > 0.0:
            gl.glBlendFunc(gl.GL_DST_COLOR, gl.GL_SRC_COLOR)
            id_ = self.renderEngine.getTexture('terrain.png')
            gl.glBindTexture(gl.GL_TEXTURE_2D, id_)
            gl.glColor4f(1.0, 1.0, 1.0, 0.5)
            gl.glPushMatrix()
            block = self.worldObj.getBlockId(h.blockX, h.blockY, h.blockZ)
            block = blocks.blocksList[block] if block > 0 else None
            t.startDrawingQuads()
            t.disableColor()
            if not block:
                block = blocks.stone

            self.globalRenderBlocks.overrideBlockTexture = 240 + int(self.damagePartialTime * 10.0)
            self.globalRenderBlocks.renderBlockByRenderType(block, h.blockX,
                                                            h.blockY, h.blockZ)
            self.globalRenderBlocks.overrideBlockTexture = -1
            t.draw()
            gl.glDepthMask(True)
            gl.glPopMatrix()

        gl.glDisable(gl.GL_BLEND)
        gl.glDisable(gl.GL_ALPHA_TEST)

    def markBlocksForUpdate(self, x0, y0, z0, x1, y1, z1):
        x0 //= self.CHUNK_SIZE
        x1 //= self.CHUNK_SIZE
        y0 //= self.CHUNK_SIZE
        y1 //= self.CHUNK_SIZE
        z0 //= self.CHUNK_SIZE
        z1 //= self.CHUNK_SIZE

        if x0 < 0: x0 = 0
        if y0 < 0: y0 = 0
        if z0 < 0: z0 = 0
        if x1 >= self.__renderChunksWide: x1 = self.__renderChunksWide - 1
        if y1 >= self.__renderChunksTall: y1 = self.__renderChunksTall - 1
        if z1 >= self.__renderChunksDeep: z1 = self.__renderChunksDeep - 1

        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                for z in range(z0, z1 + 1):
                    i = (z * self.__renderChunksTall + y) * self.__renderChunksWide + x
                    chunk = self.worldRenderers[i]
                    if not chunk.needsUpdate:
                        chunk.needsUpdate = True
                        self.worldRenderersToUpdate.append(chunk)
