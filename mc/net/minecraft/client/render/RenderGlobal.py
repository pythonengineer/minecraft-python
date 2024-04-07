from mc.net.minecraft.game.level.block.Blocks import blocks
from mc.net.minecraft.game.entity.player.EntityPlayer import EntityPlayer
from mc.net.minecraft.client.render.EntitySorter import EntitySorter
from mc.net.minecraft.client.render.Tessellator import tessellator
from mc.net.minecraft.client.render.WorldRenderer import WorldRenderer
from mc.net.minecraft.client.render.RenderManager import RenderManager
from mc.net.minecraft.client.render.RenderSorter import RenderSorter
from mc.net.minecraft.client.render.RenderBlocks import RenderBlocks
from mc.CompatibilityShims import BufferUtils, getMillis
from pyglet import gl
from functools import cmp_to_key

import math

class RenderGlobal:
    MAX_REBUILDS_PER_FRAME = 3
    CHUNK_SIZE = 16

    def __init__(self, minecraft, renderEngine):
        self.__mc = minecraft
        self.__renderEngine = renderEngine
        self.__worldObj = None
        self.__renderIntBuffer = BufferUtils.createIntBuffer(65536)
        self.__worldRenderersToUpdate = []
        self.__sortedWorldRenderers = []
        self.__worldRenderers = []
        self.__globalRenderBlocks = None
        self.renderManager = RenderManager()
        self.__chunkBuffer = [0] * 50000
        self.__cloudOffsetX = 0
        self.__prevSortX = -9999.0
        self.__prevSortY = -9999.0
        self.__prevSortZ = -9999.0
        self.damagePartialTime = 0.0
        self.__glGenList = gl.glGenLists(2)
        self.__glRenderListBase = gl.glGenLists(524288)

    def setWorld(self, world):
        if self.__worldObj:
            self.__worldObj.removeWorldAccess(self)

        self.renderManager.setWorld(world)
        self.__worldObj = world
        self.__globalRenderBlocks = RenderBlocks(tessellator, world)
        if world:
            world.addWorldAccess(self)
            self.loadRenderers()

    def loadRenderers(self):
        if self.__worldRenderers:
            for chunk in self.__worldRenderers:
                chunk.stopRendering()

        self.__renderChunksWide = self.__worldObj.width // self.CHUNK_SIZE
        self.__renderChunksTall = self.__worldObj.height // self.CHUNK_SIZE
        self.__renderChunksDeep = self.__worldObj.length // self.CHUNK_SIZE
        self.__worldRenderers = [None] * self.__renderChunksWide * self.__renderChunksTall * self.__renderChunksDeep
        self.__sortedWorldRenderers = [None] * self.__renderChunksWide * self.__renderChunksTall * self.__renderChunksDeep

        lists = 0
        for x in range(self.__renderChunksWide):
            for y in range(self.__renderChunksTall):
                for z in range(self.__renderChunksDeep):
                    i = (z * self.__renderChunksTall + y) * self.__renderChunksWide + x
                    self.__worldRenderers[i] = WorldRenderer(self.__worldObj, x << 4, y << 4,
                                                             z << 4, RenderGlobal.CHUNK_SIZE,
                                                             self.__glRenderListBase + lists)
                    self.__sortedWorldRenderers[i] = self.__worldRenderers[i]
                    lists += 2

        for chunk in self.__worldRenderersToUpdate:
            chunk.needsUpdate = False

        self.__worldRenderersToUpdate.clear()
        gl.glNewList(self.__glGenList, gl.GL_COMPILE)
        gl.glColor4f(0.5, 0.5, 0.5, 1.0)
        t = tessellator
        y = self.__worldObj.getGroundLevel()
        s = 128
        if s > self.__worldObj.width:
            s = self.__worldObj.width
        if s > self.__worldObj.length:
            s = self.__worldObj.length
        d = 2048 // s
        t.startDrawingQuads()
        for xx in range(-s * d, self.__worldObj.width + s * d, s):
            for zz in range(-s * d, self.__worldObj.length + s * d, s):
                yy = y
                if xx >= 0 and zz >= 0 and xx < self.__worldObj.width and zz < self.__worldObj.length:
                    yy = 0.0

                t.addVertexWithUV(xx + 0, yy, zz + s, 0.0, s)
                t.addVertexWithUV(xx + s, yy, zz + s, s, s)
                t.addVertexWithUV(xx + s, yy, zz + 0, s, 0.0)
                t.addVertexWithUV(xx + 0, yy, zz + 0, 0.0, 0.0)

        t.draw()
        gl.glColor3f(0.8, 0.8, 0.8)
        t.startDrawingQuads()

        for xx in range(0, self.__worldObj.width, s):
            t.addVertexWithUV(xx + 0, 0.0, 0.0, 0.0, 0.0)
            t.addVertexWithUV(xx + s, 0.0, 0.0, s, 0.0)
            t.addVertexWithUV(xx + s, y, 0.0, s, y)
            t.addVertexWithUV(xx + 0, y, 0.0, 0.0, y)

            t.addVertexWithUV(xx + 0, y, self.__worldObj.length, 0.0, y)
            t.addVertexWithUV(xx + s, y, self.__worldObj.length, s, y)
            t.addVertexWithUV(xx + s, 0.0, self.__worldObj.length, s, 0.0)
            t.addVertexWithUV(xx + 0, 0.0, self.__worldObj.length, 0.0, 0.0)

        gl.glColor3f(0.6, 0.6, 0.6)

        for zz in range(0, self.__worldObj.length, s):
            t.addVertexWithUV(0.0, y, zz + 0, 0.0, 0.0)
            t.addVertexWithUV(0.0, y, zz + s, s, 0.0)
            t.addVertexWithUV(0.0, 0.0, zz + s, s, y)
            t.addVertexWithUV(0.0, 0.0, zz + 0, 0.0, y)

            t.addVertexWithUV(self.__worldObj.width, 0.0, zz + 0, 0.0, y)
            t.addVertexWithUV(self.__worldObj.width, 0.0, zz + s, s, y)
            t.addVertexWithUV(self.__worldObj.width, y, zz + s, s, 0.0)
            t.addVertexWithUV(self.__worldObj.width, y, zz + 0, 0.0, 0.0)

        t.draw()
        gl.glEndList()
        gl.glNewList(self.__glGenList + 1, gl.GL_COMPILE)
        gl.glColor3f(1.0, 1.0, 1.0)
        y = self.__worldObj.getWaterLevel()
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        t = tessellator
        s = 128
        if s > self.__worldObj.width:
            s = self.__worldObj.width
        if s > self.__worldObj.length:
            s = self.__worldObj.length

        d = 2048 // s
        t.startDrawingQuads()

        for xx in range(-s * d, self.__worldObj.width + s * d, s):
            for zz in range(-s * d, self.__worldObj.length + s * d, s):
                yy = y - 0.1
                if xx < 0 or zz < 0 or xx >= self.__worldObj.width or zz >= self.__worldObj.length:
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
        self.__markBlocksForUpdate(0, 0, 0, self.__worldObj.width, self.__worldObj.height, self.__worldObj.length)

    def renderEntities(self, vec, clippingHelper, a):
        self.renderManager.cacheActiveRenderInfo(a)
        eMap = self.__worldObj.entityMap
        for x in range(eMap.width):
            x0 = (x << 4) - 2
            x1 = (x + 1 << 4) + 2
            for y in range(eMap.depth):
                y0 = (y << 4) - 2
                y1 = (y + 1 << 4) + 2
                for z in range(eMap.height):
                    entities = eMap.entityGrid[(z * eMap.depth + y) * eMap.width + x]
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
                                    self.renderManager.renderEntityWithPosYaw(
                                        entity, self.__renderEngine, a
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
            gl.glBindTexture(gl.GL_TEXTURE_2D, self.__renderEngine.getTexture('terrain.png'))
            self.__renderIntBuffer.glCallLists(self.__renderIntBuffer.capacity(), gl.GL_INT)

        return self.__renderIntBuffer.remaining()

    def renderAllRenderLists(self):
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.__renderEngine.getTexture('terrain.png'))
        self.__renderIntBuffer.glCallLists(self.__renderIntBuffer.capacity(), gl.GL_INT)

    def updateClouds(self):
        self.__cloudOffsetX += 1

    def renderClouds(self, partialTicks):
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.__renderEngine.getTexture('clouds.png'))
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        r = (self.__worldObj.cloudColor >> 16 & 0xFF) / 255.0
        g = (self.__worldObj.cloudColor >> 8 & 0xFF) / 255.0
        b = (self.__worldObj.cloudColor & 0xFF) / 255.0
        if self.__mc.options.anaglyph:
            nr = (r * 30.0 + g * 59.0 + b * 11.0) / 100.0
            g = (r * 30.0 + g * 70.0) / 100.0
            b = (r * 30.0 + b * 70.0) / 100.0
            r = nr

        t = tessellator
        scale = 0.5 / 1024
        y = self.__worldObj.height + 2.
        u = (self.__cloudOffsetX + partialTicks) * scale * 0.03
        t.startDrawingQuads()
        t.setColorOpaque_F(r, g, b)

        for x in range(-2048, self.__worldObj.width + 2048, 512):
            for z in range(-2048, self.__worldObj.height + 2048, 512):
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
        r = (self.__worldObj.skyColor >> 16 & 0xFF) / 255.0
        g = (self.__worldObj.skyColor >> 8 & 0xFF) / 255.0
        b = (self.__worldObj.skyColor & 0xFF) / 255.0
        if self.__mc.options.anaglyph:
            nr = (r * 30.0 + g * 59.0 + b * 11.0) / 100.0
            g = (r * 30.0 + g * 70.0) / 100.0
            b = (r * 30.0 + b * 70.0) / 100.0
            r = nr

        t.setColorOpaque_F(r, g, b)
        y = self.__worldObj.height + 10.

        for x in range(-2048, self.__worldObj.width + 2048, 512):
            for z in range(-2048, self.__worldObj.height + 2048, 512):
                t.addVertex(x, y, z)
                t.addVertex(x + 512., y, z)
                t.addVertex(x + 512., y, z + 512.)
                t.addVertex(x, y, z + 512.)

        t.draw()
        gl.glEnable(gl.GL_TEXTURE_2D)

    def oobGroundRenderer(self):
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.__renderEngine.getTexture('rock.png'))
        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glCallList(self.__glGenList)

    def oobWaterRenderer(self):
        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glEnable(gl.GL_BLEND)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.__renderEngine.getTexture('water.png'))
        gl.glCallList(self.__glGenList + 1)
        gl.glDisable(gl.GL_BLEND)

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

    def drawBlockBreaking(self, h, mode, item):
        t = tessellator
        gl.glEnable(gl.GL_BLEND)
        gl.glEnable(gl.GL_ALPHA_TEST)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE)
        gl.glColor4f(1.0, 1.0, 1.0, (math.sin(getMillis() / 100.0) * 0.2 + 0.4) * 0.5)
        if self.damagePartialTime > 0.0:
            gl.glBlendFunc(gl.GL_DST_COLOR, gl.GL_SRC_COLOR)
            id_ = self.__renderEngine.getTexture('terrain.png')
            gl.glBindTexture(gl.GL_TEXTURE_2D, id_)
            gl.glColor4f(1.0, 1.0, 1.0, 0.5)
            gl.glPushMatrix()
            block = self.__worldObj.getBlockId(h.blockX, h.blockY, h.blockZ)
            block = blocks.blocksList[block] if block > 0 else None
            t.startDrawingQuads()
            t.disableColor()
            if not block:
                block = blocks.stone

            self.__globalRenderBlocks.renderBlockAllFacesHit(
                block, h.blockX, h.blockY, h.blockZ,
                240 + int(self.damagePartialTime * 10.0)
            )
            t.draw()
            gl.glDepthMask(True)
            gl.glPopMatrix()

        gl.glDisable(gl.GL_BLEND)
        gl.glDisable(gl.GL_ALPHA_TEST)

    def drawSelectionBox(self, h, mode):
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glColor4f(0.0, 0.0, 0.0, 0.4)
        gl.glLineWidth(2.0)
        gl.glDisable(gl.GL_TEXTURE_2D)
        gl.glDepthMask(False)
        block = self.__worldObj.getBlockId(h.blockX, h.blockY, h.blockZ)
        if block > 0:
            blocks.blocksList[block].getSelectedBoundingBoxFromPool(
                self.__mc.objectMouseOver.blockX, self.__mc.objectMouseOver.blockY,
                self.__mc.objectMouseOver.blockZ
            ).expand(0.002, 0.002, 0.002).render()

        gl.glDepthMask(True)
        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glDisable(gl.GL_BLEND)

    def __markBlocksForUpdate(self, x0, y0, z0, x1, y1, z1):
        x0 //= RenderGlobal.CHUNK_SIZE
        x1 //= RenderGlobal.CHUNK_SIZE
        y0 //= RenderGlobal.CHUNK_SIZE
        y1 //= RenderGlobal.CHUNK_SIZE
        z0 //= RenderGlobal.CHUNK_SIZE
        z1 //= RenderGlobal.CHUNK_SIZE

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

    def markBlockAndNeighborsNeedsUpdate(self, x, y, z):
        self.__markBlocksForUpdate(x - 1, y - 1, z - 1, x + 1, y + 1, z + 1)

    def markBlockRangeNeedsUpdate(self, x0, y0, z0, x1, y1, z1):
        self.__markBlocksForUpdate(x0 - 1, y0 - 1, z0 - 1, x1 + 1, y1 + 1, z1 + 1)

    def clipRenderersByFrustrum(self, clippingHelper):
        for chunk in self.__worldRenderers:
            chunk.updateInFrustrum(clippingHelper)

    def playSound(self, sound, x, y, z, volume, pitch):
        self.__mc.sndManager.playSoundAtPos(sound, x, y, z, volume, pitch)
