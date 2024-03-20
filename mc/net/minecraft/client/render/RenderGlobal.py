from mc.net.minecraft.game.level.block.Blocks import blocks
from mc.net.minecraft.game.entity.player.EntityPlayer import EntityPlayer
from mc.net.minecraft.client.render.EntitySorter import EntitySorter
from mc.net.minecraft.client.render.Tessellator import tessellator
from mc.net.minecraft.client.render.WorldRenderer import WorldRenderer
from mc.net.minecraft.client.render.RenderManager import RenderManager
from mc.net.minecraft.client.render.RenderSorter import RenderSorter
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
        self.__renderIntBuffer = BufferUtils.createIntBuffer(65536)
        self.__worldRenderersToUpdate = []
        self.__sortedWorldRenderers = []
        self.__worldRenderers = []
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
        if self.__worldRenderers:
            for chunk in self.__worldRenderers:
                chunk.stopRendering()

        self.__renderChunksWide = self.worldObj.width // self.CHUNK_SIZE
        self.__renderChunksTall = self.worldObj.height // self.CHUNK_SIZE
        self.__renderChunksDeep = self.worldObj.length // self.CHUNK_SIZE
        self.__worldRenderers = [None] * self.__renderChunksWide * self.__renderChunksTall * self.__renderChunksDeep
        self.__sortedWorldRenderers = [None] * self.__renderChunksWide * self.__renderChunksTall * self.__renderChunksDeep

        lists = 0
        for x in range(self.__renderChunksWide):
            for y in range(self.__renderChunksTall):
                for z in range(self.__renderChunksDeep):
                    i = (z * self.__renderChunksTall + y) * self.__renderChunksWide + x
                    self.__worldRenderers[i] = WorldRenderer(self.worldObj, x << 4, y << 4,
                                                             z << 4,
                                                             self.__glRenderListBase + lists)
                    self.__sortedWorldRenderers[i] = self.__worldRenderers[i]
                    lists += 2

        for chunk in self.__worldRenderersToUpdate:
            chunk.needsUpdate = False

        self.__worldRenderersToUpdate.clear()
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

    def renderEntities(self, vec, clippingHelper, a):
        player = self.worldObj.getPlayerEntity()
        self.renderManager.playerViewY = player.prevRotationYaw + (player.rotationYaw - player.prevRotationYaw) * a

        for x in range(self.worldObj.entityMap.xSlot):
            x0 = (x << 4) - 2
            x1 = (x + 1 << 4) + 2
            for y in range(self.worldObj.entityMap.ySlot):
                y0 = (y << 4) - 2
                y1 = (y + 1 << 4) + 2
                for z in range(self.worldObj.entityMap.zSlot):
                    entities = self.worldObj.entityMap.entityGrid[(z * self.worldObj.entityMap.ySlot + y) * self.worldObj.entityMap.xSlot + x]
                    if not entities:
                        continue

                    z0 = (z << 4) - 2
                    z1 = (z + 1 << 4) + 2
                    if clippingHelper.isBoundingBoxInFrustrum(x0, y0, z0, x1, y1, z1):
                        exists = clippingHelper.isBoundingBoxFullyInFrustrum(x0, y0, z0,
                                                                             x1, y1, z1)
                        for entity in entities:
                            if entity.shouldRender(vec) and (exists or clippingHelper.isVisible(entity.boundingBox)):
                                if not isinstance(entity, EntityPlayer):
                                    xd = entity.lastTickPosX + (entity.posX - entity.lastTickPosX) * a
                                    yd = entity.lastTickPosY + (entity.posY - entity.lastTickPosY) * a
                                    zd = entity.lastTickPosZ + (entity.posZ - entity.lastTickPosZ) * a
                                    light = self.worldObj.getBlockLightValue(
                                        int(xd),
                                        int(yd + entity.bbHeight * 2.0 / 3.0),
                                        int(zd)
                                    )
                                    gl.glColor3f(light, light, light)
                                    self.renderManager.renderEntityWithPosYaw(
                                        entity, self.renderEngine, xd, yd, zd, 1.0, a
                                    )

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

        self.__renderIntBuffer.clear()
        self.__renderIntBuffer.putOffset(self.__chunkBuffer, 0, startingIndex)
        self.__renderIntBuffer.flip()
        if self.__renderIntBuffer.remaining() > 0:
            gl.glBindTexture(gl.GL_TEXTURE_2D, self.renderEngine.getTexture('terrain.png'))
            self.__renderIntBuffer.glCallLists(self.__renderIntBuffer.capacity(), gl.GL_INT)

        return self.__renderIntBuffer.remaining()

    def renderAllRenderLists(self):
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.renderEngine.getTexture('terrain.png'))
        self.__renderIntBuffer.glCallLists(self.__renderIntBuffer.capacity(), gl.GL_INT)

    def updateRenderers(self, player):
        self.__worldRenderersToUpdate = sorted(
            self.__worldRenderersToUpdate,
            key=cmp_to_key(RenderSorter(player).compare)
        )

        last = len(self.__worldRenderersToUpdate) - 1
        for i in range(min(len(self.__worldRenderersToUpdate),
                       RenderGlobal.MAX_REBUILDS_PER_FRAME)):
            chunk = self.__worldRenderersToUpdate.pop(last - i)
            chunk.updateRenderer()
            chunk.needsUpdate = False

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
        scale = 0.5 / 1024
        y = self.worldObj.height + 2.
        u = (self.cloudOffsetX + partialTicks) * scale * 0.03
        t.startDrawingQuads()
        t.setColorOpaque_F(r, g, b)

        for x in range(-2048, self.worldObj.width + 2048, 512):
            for z in range(-2048, self.worldObj.height + 2048, 512):
                t.addVertexWithUV(x, y, z + 512., x * scale + u, (z + 512.) * scale)
                t.addVertexWithUV(x + 512., y, z + 512., (x + 512.) * scale + u, (z + 512.) * scale)
                t.addVertexWithUV(x + 512., y, z, (x + 512.) * scale + u, z * scale)
                t.addVertexWithUV(x, y, z, x * scale + u, z * scale)
                t.addVertexWithUV(x, y, z, x * scale + u, z * scale)
                t.addVertexWithUV(x + 512., y, z, (x + 512.) * scale + u, z * scale)
                t.addVertexWithUV(x + 512., y, z + 512., (x + 512.) * scale + u, (z + 512.) * scale)
                t.addVertexWithUV(x, y, z + 512., x * scale + u, (z + 512.) * scale)

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
        y = self.worldObj.height + 10.

        for x in range(-2048, self.worldObj.width + 2048, 512):
            for z in range(-2048, self.worldObj.height + 2048, 512):
                t.addVertex(x, y, z)
                t.addVertex(x + 512., y, z)
                t.addVertex(x + 512., y, z + 512.)
                t.addVertex(x, y, z + 512.)

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
                    chunk = self.__worldRenderers[i]
                    if not chunk.needsUpdate:
                        chunk.needsUpdate = True
                        self.__worldRenderersToUpdate.append(chunk)

    def clipRenderersByFrustrum(self, clippingHelper):
        for chunk in self.__worldRenderers:
            chunk.updateInFrustrum(clippingHelper)
