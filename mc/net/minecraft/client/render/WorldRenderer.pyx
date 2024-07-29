# cython: language_level=3

cimport cython

from mc.net.minecraft.client.render.Frustum cimport Frustum
from mc.net.minecraft.client.render.Tessellator cimport Tessellator
from mc.net.minecraft.client.render.Tessellator import tessellator
from mc.net.minecraft.client.render.RenderBlocks cimport RenderBlocks
from mc.net.minecraft.client.render.entity.RenderItem import RenderItem
from mc.net.minecraft.game.level.block.Blocks import blocks
from mc.net.minecraft.game.level.block.Block cimport Block
from mc.net.minecraft.game.level.World cimport World
from mc.net.minecraft.game.physics.AxisAlignedBB cimport AxisAlignedBB
from pyglet import gl

cdef int WorldRenderer_chunksUpdates = 0

@cython.final
cdef class WorldRenderer:

    @property
    def chunksUpdates(self):
        return WorldRenderer_chunksUpdates

    @chunksUpdates.setter
    def chunksUpdates(self, x):
        global WorldRenderer_chunksUpdates
        WorldRenderer_chunksUpdates = x

    def __cinit__(self):
        self.__t = tessellator
        self.__glRenderList = -1
        self.isInFrustum = False
        self.needsUpdate = False

    def __init__(self, World world, int posX, int posY, int posZ,
                 int size, int lists, bint fake=False):
        if fake:
            return

        self.__renderBlocks = RenderBlocks(tessellator, world)
        self.__worldObj = world
        self.__posX = posX
        self.__posY = posY
        self.__posZ = posZ
        self.__sizeWidth = self.__sizeHeight = self.__sizeDepth = 16
        self.__posXPlus = posX + self.__sizeWidth // 2
        self.__posYPlus = posY + self.__sizeHeight // 2
        self.__posZPlus = posZ + self.__sizeDepth // 2

        self.__rendererBoundingBox = AxisAlignedBB(
            posX, posY, posZ, posX + self.__sizeWidth, posY + self.__sizeHeight,
            posZ + self.__sizeDepth
        ).expand(2.0, 2.0, 2.0)

        self.__glRenderList = lists
        self.__setDontDraw()

        gl.glDisable(gl.GL_TEXTURE_2D)
        gl.glNewList(lists + 2, gl.GL_COMPILE)
        RenderItem.renderOffsetAABB(self.__rendererBoundingBox)
        gl.glEndList()
        gl.glEnable(gl.GL_TEXTURE_2D)

    cdef updateRenderer(self):
        cdef int layer, x0, y0, z0, xx, yy, zz, x, y, z, blockIdx, blockId
        cdef bint nextLayer, renderPass
        cdef Block block

        self.chunksUpdates += 1

        x0 = self.__posX
        y0 = self.__posY
        z0 = self.__posZ
        xx = self.__posX + self.__sizeWidth
        yy = self.__posY + self.__sizeHeight
        zz = self.__posZ + self.__sizeDepth

        for layer in range(2):
            self.__skipRenderPass[layer] = True

        for layer in range(2):
            nextLayer = False
            renderPass = False

            self.__t.startDrawingQuads()
            gl.glNewList(self.__glRenderList + layer, gl.GL_COMPILE)

            for y in range(y0, yy):
                for z in range(z0, zz):
                    blockIdx = (y * self.__worldObj.length + z) * self.__worldObj.width + x0
                    for x in range(x0, xx):
                        blockId = self.__worldObj.blocks[blockIdx] & 255
                        blockIdx += 1
                        if blockId > 0:
                            block = blocks.blocksList[blockId]
                            if block.getRenderBlockPass() != layer:
                                nextLayer = True
                            else:
                                renderPass |= self.__renderBlocks.renderBlockByRenderType(block, x, y, z)

            self.__t.draw()
            gl.glEndList()
            if renderPass:
                self.__skipRenderPass[layer] = False

            if not nextLayer:
                break

    cpdef float distanceToEntitySquared(self, player):
        cdef float xd = player.posX - self.__posXPlus
        cdef float yd = player.posY - self.__posYPlus
        cdef float zd = player.posZ - self.__posZPlus
        return xd * xd + yd * yd + zd * zd

    cdef __setDontDraw(self):
        cdef int layer
        for layer in range(2):
            self.__skipRenderPass[layer] = True

    def stopRendering(self):
        self.__setDontDraw()
        self.__worldObj = None

    cdef getGLCallListForPass(self, int* chunkBuffer, int startingIndex, int renderPass):
        if not self.isInFrustum:
            return startingIndex

        if not self.__skipRenderPass[renderPass]:
            chunkBuffer[startingIndex] = self.__glRenderList + renderPass
            startingIndex += 1

        return startingIndex

    cdef updateInFrustum(self, Frustum frustum):
        self.isInFrustum = frustum.isVisible(self.__rendererBoundingBox)
