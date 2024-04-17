# cython: language_level=3
# cython: cdivision=True

from mc.net.minecraft.client.render.Tessellator cimport Tessellator
from mc.net.minecraft.game.level.block.Block cimport Block
from mc.net.minecraft.game.level.block.Blocks import blocks
from mc.net.minecraft.game.level.World cimport World
from pyglet import gl

cdef class RenderBlocks:

    def __init__(self, Tessellator t, World world=None):
        self.__tessellator = t
        self.__blockAccess = world
        self.__overrideBlockTexture = -1
        self.__flipTexture = False

    def renderBlockAllFacesHit(self, Block block, int x, int y, int z, int tex):
        self.__overrideBlockTexture = tex
        self.renderBlockByRenderType(block, x, y, z)
        self.__overrideBlockTexture = -1

    def renderBlockAllFaces(self, Block block, int x, int y, int z):
        self.__flipTexture = True
        self.renderBlockByRenderType(block, x, y, z)
        self.__flipTexture = False

    cdef bint renderBlockByRenderType(self, Block block, int x, int y, int z):
        cdef int renderType
        cdef bint layerOk
        cdef float b

        renderType = block.getRenderType()
        if renderType == 0:
            layerOk = False
            if self.__flipTexture or block.shouldSideBeRendered(self.__blockAccess, x, y - 1, z, 0):
                b = block.getBlockBrightness(self.__blockAccess, x, y - 1, z)
                self.__tessellator.setColorOpaque_F(0.5 * b, 0.5 * b, 0.5 * b)
                self.__renderBlockBottom(block, x, y, z, block.getBlockTexture(0))
                layerOk = True
            if self.__flipTexture or block.shouldSideBeRendered(self.__blockAccess, x, y + 1, z, 1):
                b = block.getBlockBrightness(self.__blockAccess, x, y + 1, z)
                self.__tessellator.setColorOpaque_F(b, b, b)
                self.__renderBlockTop(block, x, y, z, block.getBlockTexture(1))
                layerOk = True
            if self.__flipTexture or block.shouldSideBeRendered(self.__blockAccess, x, y, z - 1, 2):
                b = block.getBlockBrightness(self.__blockAccess, x, y, z - 1)
                self.__tessellator.setColorOpaque_F(0.8 * b, 0.8 * b, 0.8 * b)
                self.__renderBlockNorth(block, x, y, z, block.getBlockTexture(2))
                layerOk = True
            if self.__flipTexture or block.shouldSideBeRendered(self.__blockAccess, x, y, z + 1, 3):
                b = block.getBlockBrightness(self.__blockAccess, x, y, z + 1)
                self.__tessellator.setColorOpaque_F(0.8 * b, 0.8 * b, 0.8 * b)
                self.__renderBlockSouth(block, x, y, z, block.getBlockTexture(3))
                layerOk = True
            if self.__flipTexture or block.shouldSideBeRendered(self.__blockAccess, x - 1, y, z, 4):
                b = block.getBlockBrightness(self.__blockAccess, x - 1, y, z)
                self.__tessellator.setColorOpaque_F(0.6 * b, 0.6 * b, 0.6 * b)
                self.__renderBlockWest(block, x, y, z, block.getBlockTexture(4))
                layerOk = True
            if self.__flipTexture or block.shouldSideBeRendered(self.__blockAccess, x + 1, y, z, 5):
                b = block.getBlockBrightness(self.__blockAccess, x + 1, y, z)
                self.__tessellator.setColorOpaque_F(0.6 * b, 0.6 * b, 0.6 * b)
                self.__renderBlockEast(block, x, y, z, block.getBlockTexture(5))
                layerOk = True

            return layerOk
        elif renderType == 1:
            b = block.getBlockBrightness(self.__blockAccess, x, y, z)
            self.__tessellator.setColorOpaque_F(b, b, b)
            self.__renderBlockPlant(block, x, y, z)
            return True
        elif renderType == 2:
            b = block.getBlockBrightness(self.__blockAccess, x, y, z)
            self.__tessellator.setColorOpaque_F(b, b, b)
            if self.__blockAccess.isBlockNormalCube(x - 1, y, z):
                self.__renderBlockTorch(block, x, y + 0.2, z, -0.5, 0.0)
            elif self.__blockAccess.isBlockNormalCube(x + 1, y, z):
                self.__renderBlockTorch(block, x, y + 0.2, z, 0.5, 0.0)
            elif self.__blockAccess.isBlockNormalCube(x, y, z - 1):
                self.__renderBlockTorch(block, x, y + 0.2, z, 0.0, -0.5)
            elif self.__blockAccess.isBlockNormalCube(x, y, z + 1):
                self.__renderBlockTorch(block, x, y + 0.2, z, 0.0, 0.5)
            else:
                self.__renderBlockTorch(block, x, y, z, 0.0, 0.0)

            return True
        elif renderType == 3:
            b = block.getBlockBrightness(self.__blockAccess, x, y, z)
            self.__tessellator.setColorOpaque_F(b, b, b)
            self.__renderBlockFire(block, x, y, z)
            return True
        else:
            return False

    cdef __renderBlockFire(self, Block block, int x, int y, int z):
        cdef int tex, xt
        cdef float u0, u1, v0, v1, oldu1, x0, x1, x2, x3, z0, z1, z2, z3
        cdef Block fire

        fire = blocks.fire
        tex = block.getBlockTexture(0)
        if self.__overrideBlockTexture >= 0:
            tex = self.__overrideBlockTexture

        xt = (tex & 15) << 4
        tex &= 240
        u0 = xt / 256.0
        u1 = (xt + 15.99) / 256.0
        v0 = tex / 256.0
        v1 = (tex + 15.99) / 256.0
        if not self.__blockAccess.isBlockNormalCube(x, y - 1, z) and \
           not fire.canBlockCatchFire(self.__blockAccess, x, y - 1, z):
            if x + y + z & 1 == 1:
                u0 = xt / 256.0
                u1 = (xt + 15.99) / 256.0
                v0 = (tex + 16) / 256.0
                v1 = (tex + 15.99 + 16.0) / 256.0

            if x // 2 + y // 2 + z // 2 & 1 == 1:
                oldu1 = u1
                u1 = u0
                u0 = oldu1

            if fire.canBlockCatchFire(self.__blockAccess, x - 1, y, z):
                self.__tessellator.addVertexWithUV(x + 0.2, y + 1.4 + 1.0 / 16.0,
                                                   z + 1, u1, v0)
                self.__tessellator.addVertexWithUV(x, y + 1.0 / 16.0, z + 1, u1, v1)
                self.__tessellator.addVertexWithUV(x, y + 1.0 / 16.0, z, u0, v1)
                self.__tessellator.addVertexWithUV(x + 0.2, y + 1.4 + 1.0 / 16.0,
                                                   z, u0, v0)
                self.__tessellator.addVertexWithUV(x + 0.2, y + 1.4 + 1.0 / 16.0,
                                                   z, u0, v0)
                self.__tessellator.addVertexWithUV(x, y + 1.0 / 16.0, z, u0, v1)
                self.__tessellator.addVertexWithUV(x, y + 1.0 / 16.0, z + 1, u1, v1)
                self.__tessellator.addVertexWithUV(x + 0.2, y + 1.4 + 1.0 / 16.0,
                                                   z + 1, u1, v0)
            if fire.canBlockCatchFire(self.__blockAccess, x + 1, y, z):
                self.__tessellator.addVertexWithUV((x + 1) - 0.2, y + 1.4 + 1.0 / 16.0,
                                                   z, u0, v0)
                self.__tessellator.addVertexWithUV(x + 1, y + 1.0 / 16.0, z, u0, v1)
                self.__tessellator.addVertexWithUV(x + 1, y + 1.0 / 16.0, z + 1, u1, v1)
                self.__tessellator.addVertexWithUV((x + 1) - 0.2, y + 1.4 + 1.0 / 16.0,
                                                   z + 1, u1, v0)
                self.__tessellator.addVertexWithUV((x + 1) - 0.2, y + 1.4 + 1.0 / 16.0,
                                                   z + 1, u1, v0)
                self.__tessellator.addVertexWithUV(x + 1, y + 1.0 / 16.0, z + 1, u1, v1)
                self.__tessellator.addVertexWithUV(x + 1, y + 1.0 / 16.0, z, u0, v1)
                self.__tessellator.addVertexWithUV((x + 1) - 0.2, y + 1.4 + 1.0 / 16.0,
                                                   z, u0, v0)
            if fire.canBlockCatchFire(self.__blockAccess, x, y, z - 1):
                self.__tessellator.addVertexWithUV(x, y + 1.4 + 1.0 / 16.0,
                                                   z + 0.2, u1, v0)
                self.__tessellator.addVertexWithUV(x, y + 1.0 / 16.0, z, u1, v1)
                self.__tessellator.addVertexWithUV(x + 1, y + 1.0 / 16.0, z, u0, v1)
                self.__tessellator.addVertexWithUV(x + 1, y + 1.4 + 1.0 / 16.0,
                                                   z + 0.2, u0, v0)
                self.__tessellator.addVertexWithUV(x + 1, y + 1.4 + 1.0 / 16.0,
                                                   z + 0.2, u0, v0)
                self.__tessellator.addVertexWithUV(x + 1, y + 1.0 / 16.0, z, u0, v1)
                self.__tessellator.addVertexWithUV(x, y + 1.0 / 16.0, z, u1, v1)
                self.__tessellator.addVertexWithUV(x, y + 1.4 + 1.0 / 16.0, z + 0.2,
                                                   u1, v0)
            if fire.canBlockCatchFire(self.__blockAccess, x, y, z + 1):
                self.__tessellator.addVertexWithUV(x + 1, y + 1.4 + 1.0 / 16.0,
                                                   (z + 1) - 0.2, u0, v0)
                self.__tessellator.addVertexWithUV(x + 1, y + 1.0 / 16.0,
                                                   z + 1, u0, v1)
                self.__tessellator.addVertexWithUV(x, y + 1.0 / 16.0, z + 1, u1, v1)
                self.__tessellator.addVertexWithUV(x, y + 1.4 + 1.0 / 16.0,
                                                   (z + 1) - 0.2, u1, v0)
                self.__tessellator.addVertexWithUV(x, y + 1.4 + 1.0 / 16.0,
                                                   (z + 1) - 0.2, u1, v0)
                self.__tessellator.addVertexWithUV(x, y + 1.0 / 16.0, z + 1, u1, v1)
                self.__tessellator.addVertexWithUV(x + 1, y + 1.0 / 16.0,
                                                   z + 1, u0, v1)
                self.__tessellator.addVertexWithUV(x + 1, y + 1.4 + 1.0 / 16.0,
                                                   (z + 1) - 0.2, u0, v0)
            if fire.canBlockCatchFire(self.__blockAccess, x, y + 1, z):
                x1 = x + 0.5 + 0.5
                x0 = x + 0.5 - 0.5
                z1 = z + 0.5 + 0.5
                z0 = z + 0.5 - 0.5
                u0 = xt / 256.0
                u1 = (xt + 15.99) / 256.0
                v0 = tex / 256.0
                v1 = (tex + 15.99) / 256.0
                y += 1
                if x + y + z & 1 == 0:
                    self.__tessellator.addVertexWithUV(x0, y + -0.2, z, u1, v0)
                    self.__tessellator.addVertexWithUV(x1, y, z, u1, v1)
                    self.__tessellator.addVertexWithUV(x1, y, z + 1, u0, v1)
                    self.__tessellator.addVertexWithUV(x0, y + -0.2, z + 1, u0, v0)
                    u0 = xt / 256.0
                    u1 = (xt + 15.99) / 256.0
                    v0 = (tex + 16) / 256.0
                    v1 = (tex + 15.99 + 16.0) / 256.0
                    self.__tessellator.addVertexWithUV(x1, y + -0.2, z + 1, u1, v0)
                    self.__tessellator.addVertexWithUV(x0, y, z + 1, u1, v1)
                    self.__tessellator.addVertexWithUV(x0, y, z, u0, v1)
                    self.__tessellator.addVertexWithUV(x1, y + -0.2, z, u0, v0)
                else:
                    self.__tessellator.addVertexWithUV(x, y + -0.2, z1, u1, v0)
                    self.__tessellator.addVertexWithUV(x, y, z0, u1, v1)
                    self.__tessellator.addVertexWithUV(x + 1, y, z0, u0, v1)
                    self.__tessellator.addVertexWithUV(x + 1, y + -0.2, z1, u0, v0)
                    u0 = xt / 256.0
                    u1 = (xt + 15.99) / 256.0
                    v0 = (tex + 16) / 256.0
                    v1 = (tex + 15.99 + 16.0) / 256.0
                    self.__tessellator.addVertexWithUV(x + 1, y + -0.2, z0, u1, v0)
                    self.__tessellator.addVertexWithUV(x + 1, y, z1, u1, v1)
                    self.__tessellator.addVertexWithUV(x, y, z1, u0, v1)
                    self.__tessellator.addVertexWithUV(x, y + -0.2, z0, u0, v0)
        else:
            x2 = x + 0.5 + 0.2
            x1 = x + 0.5 - 0.2
            z2 = z + 0.5 + 0.2
            z1 = z + 0.5 - 0.2
            x0 = x + 0.5 - 0.3
            x3 = x + 0.5 + 0.3
            z0 = z + 0.5 - 0.3
            z3 = z + 0.5 + 0.3
            self.__tessellator.addVertexWithUV(x0, y + 1.4, z + 1, u1, v0)
            self.__tessellator.addVertexWithUV(x2, y, z + 1, u1, v1)
            self.__tessellator.addVertexWithUV(x2, y, z, u0, v1)
            self.__tessellator.addVertexWithUV(x0, y + 1.4, z, u0, v0)
            self.__tessellator.addVertexWithUV(x3, y + 1.4, z, u1, v0)
            self.__tessellator.addVertexWithUV(x1, y, z, u1, v1)
            self.__tessellator.addVertexWithUV(x1, y, z + 1, u0, v1)
            self.__tessellator.addVertexWithUV(x3, y + 1.4, z + 1, u0, v0)
            u1 = (xt + 15.99) / 256.0
            v0 = (tex + 16) / 256.0
            v1 = (tex + 15.99 + 16.0) / 256.0
            self.__tessellator.addVertexWithUV(x + 1, y + 1.4, z3, u1, v0)
            self.__tessellator.addVertexWithUV(x + 1, y, z1, u1, v1)
            self.__tessellator.addVertexWithUV(x, y, z1, u0, v1)
            self.__tessellator.addVertexWithUV(x, y + 1.4, z3, u0, v0)
            self.__tessellator.addVertexWithUV(x, y + 1.4, z0, u1, v0)
            self.__tessellator.addVertexWithUV(x, y, z2, u1, v1)
            self.__tessellator.addVertexWithUV(x + 1, y, z2, u0, v1)
            self.__tessellator.addVertexWithUV(x + 1, y + 1.4, z0, u0, v0)
            x2 = x + 0.5 - 0.5
            x1 = x + 0.5 + 0.5
            z2 = z + 0.5 - 0.5
            z1 = z + 0.5 + 0.5
            x0 = x + 0.5 - 0.4
            x3 = x + 0.5 + 0.4
            z0 = z + 0.5 - 0.4
            z3 = z + 0.5 + 0.4
            self.__tessellator.addVertexWithUV(x0, y + 1.4, z, u0, v0)
            self.__tessellator.addVertexWithUV(x2, y, z, u0, v1)
            self.__tessellator.addVertexWithUV(x2, y, z + 1, u1, v1)
            self.__tessellator.addVertexWithUV(x0, y + 1.4, z + 1, u1, v0)
            self.__tessellator.addVertexWithUV(x3, y + 1.4, z + 1, u0, v0)
            self.__tessellator.addVertexWithUV(x1, y, z + 1, u0, v1)
            self.__tessellator.addVertexWithUV(x1, y, z, u1, v1)
            self.__tessellator.addVertexWithUV(x3, y + 1.4, z, u1, v0)
            v0 = tex / 256.0
            v1 = (tex + 15.99) / 256.0
            self.__tessellator.addVertexWithUV(x, y + 1.4, z3, u0, v0)
            self.__tessellator.addVertexWithUV(x, y, z1, u0, v1)
            self.__tessellator.addVertexWithUV(x + 1, y, z1, u1, v1)
            self.__tessellator.addVertexWithUV(x + 1, y + 1.4, z3, u1, v0)
            self.__tessellator.addVertexWithUV(x + 1, y + 1.4, z0, u0, v0)
            self.__tessellator.addVertexWithUV(x + 1, y, z2, u0, v1)
            self.__tessellator.addVertexWithUV(x, y, z2, u1, v1)
            self.__tessellator.addVertexWithUV(x, y + 1.4, z0, u1, v0)

    cdef __renderBlockTorch(self, Block block, float x, float y, float z,
                            float xOffset, float zOffset):
        cdef int tex, xt
        cdef float u0, u1, v0, v1, x0, x1, z0, z1, rot

        tex = block.getBlockTexture(0)
        if self.__overrideBlockTexture >= 0:
            tex = self.__overrideBlockTexture

        xt = (tex & 15) << 4
        tex &= 240
        u0 = xt / 256.0
        u1 = (xt + 15.99) / 256.0
        v0 = tex / 256.0
        v1 = (tex + 15.99) / 256.0
        x += 0.5
        z += 0.5
        x0 = x - 0.5
        x1 = x + 0.5
        z0 = z - 0.5
        z1 = z + 0.5
        rot = 1.0 / 16.0
        self.__tessellator.addVertexWithUV(x - rot, y + 1.0, z0, u0, v0)
        self.__tessellator.addVertexWithUV(x - rot + xOffset, y, z0 + zOffset, u0, v1)
        self.__tessellator.addVertexWithUV(x - rot + xOffset, y, z1 + zOffset, u1, v1)
        self.__tessellator.addVertexWithUV(x - rot, y + 1.0, z1, u1, v0)
        self.__tessellator.addVertexWithUV(x + rot, y + 1.0, z1, u0, v0)
        self.__tessellator.addVertexWithUV(x + xOffset + rot, y, z1 + zOffset, u0, v1)
        self.__tessellator.addVertexWithUV(x + xOffset + rot, y, z0 + zOffset, u1, v1)
        self.__tessellator.addVertexWithUV(x + rot, y + 1.0, z0, u1, v0)
        self.__tessellator.addVertexWithUV(x0, y + 1.0, z + rot, u0, v0)
        self.__tessellator.addVertexWithUV(x0 + xOffset, y, z + rot + zOffset, u0, v1)
        self.__tessellator.addVertexWithUV(x1 + xOffset, y, z + rot + zOffset, u1, v1)
        self.__tessellator.addVertexWithUV(x1, y + 1.0, z + rot, u1, v0)
        self.__tessellator.addVertexWithUV(x1, y + 1.0, z - rot, u0, v0)
        self.__tessellator.addVertexWithUV(x1 + xOffset, y, z - rot + zOffset, u0, v1)
        self.__tessellator.addVertexWithUV(x0 + xOffset, y, z - rot + zOffset, u1, v1)
        self.__tessellator.addVertexWithUV(x0, y + 1.0, z - rot, u1, v0)

    cdef __renderBlockPlant(self, Block block, float x, float y, float z):
        cdef int tex, xt
        cdef float u0, u1, v0, v1, x1, z1

        tex = block.getBlockTexture(0)
        if self.__overrideBlockTexture >= 0:
            tex = self.__overrideBlockTexture

        xt = (tex & 15) << 4
        tex &= 240
        u0 = xt / 256.0
        u1 = (xt + 15.99) / 256.0
        v0 = tex / 256.0
        v1 = (tex + 15.99) / 256.0
        x1 = x + 0.5 - 0.45
        x = x + 0.5 + 0.45
        z1 = z + 0.5 - 0.45
        z = z + 0.5 + 0.45
        self.__tessellator.addVertexWithUV(x1, y + 1.0, z1, u0, v0)
        self.__tessellator.addVertexWithUV(x1, y, z1, u0, v1)
        self.__tessellator.addVertexWithUV(x, y, z, u1, v1)
        self.__tessellator.addVertexWithUV(x, y + 1.0, z, u1, v0)
        self.__tessellator.addVertexWithUV(x, y + 1.0, z, u0, v0)
        self.__tessellator.addVertexWithUV(x, y, z, u0, v1)
        self.__tessellator.addVertexWithUV(x1, y, z1, u1, v1)
        self.__tessellator.addVertexWithUV(x1, y + 1.0, z1, u1, v0)
        self.__tessellator.addVertexWithUV(x1, y + 1.0, z, u0, v0)
        self.__tessellator.addVertexWithUV(x1, y, z, u0, v1)
        self.__tessellator.addVertexWithUV(x, y, z1, u1, v1)
        self.__tessellator.addVertexWithUV(x, y + 1.0, z1, u1, v0)
        self.__tessellator.addVertexWithUV(x, y + 1.0, z1, u0, v0)
        self.__tessellator.addVertexWithUV(x, y, z1, u0, v1)
        self.__tessellator.addVertexWithUV(x1, y, z, u1, v1)
        self.__tessellator.addVertexWithUV(x1, y + 1.0, z, u1, v0)

    cdef __renderBlockBottom(self, Block block, float x, float y, float z, int tex):
        cdef int xt
        cdef float u0, u1, v0, v1, x0, x1, y0, z0, z1

        if self.__overrideBlockTexture >= 0:
            tex = self.__overrideBlockTexture

        xt = (tex & 15) << 4
        tex &= 240
        u0 = xt / 256.0
        u1 = (xt + 15.99) / 256.0
        v0 = tex / 256.0
        v1 = (tex + 15.99) / 256.0
        x0 = x + block.minX
        x1 = x + block.maxX
        y0 = y + block.minY
        z0 = z + block.minZ
        z1 = z + block.maxZ
        self.__tessellator.addVertexWithUV(x0, y0, z1, u0, v1)
        self.__tessellator.addVertexWithUV(x0, y0, z0, u0, v0)
        self.__tessellator.addVertexWithUV(x1, y0, z0, u1, v0)
        self.__tessellator.addVertexWithUV(x1, y0, z1, u1, v1)

    cdef __renderBlockTop(self, Block block, float x, float y, float z, int tex):
        cdef int xt
        cdef float u0, u1, v0, v1, x0, x1, y1, z0, z1

        if self.__overrideBlockTexture >= 0:
            tex = self.__overrideBlockTexture

        xt = (tex & 15) << 4
        tex &= 240
        u0 = xt / 256.0
        u1 = (xt + 15.99) / 256.0
        v0 = tex / 256.0
        v1 = (tex + 15.99) / 256.0
        x0 = x + block.minX
        x1 = x + block.maxX
        y1 = y + block.maxY
        z0 = z + block.minZ
        z1 = z + block.maxZ
        self.__tessellator.addVertexWithUV(x1, y1, z1, u1, v1)
        self.__tessellator.addVertexWithUV(x1, y1, z0, u1, v0)
        self.__tessellator.addVertexWithUV(x0, y1, z0, u0, v0)
        self.__tessellator.addVertexWithUV(x0, y1, z1, u0, v1)

    cdef __renderBlockNorth(self, Block block, int x, int y, int z, int tex):
        cdef int xt
        cdef float u0, u1, v0, v1, x0, x1, y0, y1, z0

        if self.__overrideBlockTexture >= 0:
            tex = self.__overrideBlockTexture

        xt = (tex & 15) << 4
        tex &= 240
        u0 = xt / 256.0
        u1 = (xt + 15.99) / 256.0
        v0 = 0.0
        v1 = 0.0
        if block.minY >= 0.0 and block.maxY <= 1.0:
            v0 = (tex + block.minY * 15.99) / 256.0
            v1 = (tex + block.maxY * 15.99) / 256.0
        else:
            v0 = tex / 256.0
            v1 = (tex + 15.99) / 256.0

        x0 = x + block.minX
        x1 = x + block.maxX
        y0 = y + block.minY
        y1 = y + block.maxY
        z0 = z + block.minZ
        self.__tessellator.addVertexWithUV(x0, y1, z0, u1, v0)
        self.__tessellator.addVertexWithUV(x1, y1, z0, u0, v0)
        self.__tessellator.addVertexWithUV(x1, y0, z0, u0, v1)
        self.__tessellator.addVertexWithUV(x0, y0, z0, u1, v1)

    cdef __renderBlockSouth(self, Block block, int x, int y, int z, int tex):
        cdef int xt
        cdef float u0, u1, v0, v1, x0, x1, y0, y1, z1

        if self.__overrideBlockTexture >= 0:
            tex = self.__overrideBlockTexture

        xt = (tex & 15) << 4
        tex &= 240
        u0 = xt / 256.0
        u1 = (xt + 15.99) / 256.0
        v0 = 0.0
        v1 = 0.0
        if block.minY >= 0.0 and block.maxY <= 1.0:
            v0 = (tex + block.minY * 15.99) / 256.0
            v1 = (tex + block.maxY * 15.99) / 256.0
        else:
            v0 = tex / 256.0
            v1 = (tex + 15.99) / 256.0

        x0 = x + block.minX
        x1 = x + block.maxX
        y0 = y + block.minY
        y1 = y + block.maxY
        z1 = z + block.maxZ
        self.__tessellator.addVertexWithUV(x0, y1, z1, u0, v0)
        self.__tessellator.addVertexWithUV(x0, y0, z1, u0, v1)
        self.__tessellator.addVertexWithUV(x1, y0, z1, u1, v1)
        self.__tessellator.addVertexWithUV(x1, y1, z1, u1, v0)

    cdef __renderBlockWest(self, Block block, int x, int y, int z, int tex):
        cdef int xt
        cdef float u0, u1, v0, v1, x0, y0, y1, z0, z1

        if self.__overrideBlockTexture >= 0:
            tex = self.__overrideBlockTexture

        xt = (tex & 15) << 4
        tex &= 240
        u0 = xt / 256.0
        u1 = (xt + 15.99) / 256.0
        v0 = 0.0
        v1 = 0.0
        if block.minY >= 0.0 and block.maxY <= 1.0:
            v0 = (tex + block.minY * 15.99) / 256.0
            v1 = (tex + block.maxY * 15.99) / 256.0
        else:
            v0 = tex / 256.0
            v1 = (tex + 15.99) / 256.0

        x0 = x + block.minX
        y0 = y + block.minY
        y1 = y + block.maxY
        z0 = z + block.minZ
        z1 = z + block.maxZ
        self.__tessellator.addVertexWithUV(x0, y1, z1, u1, v0)
        self.__tessellator.addVertexWithUV(x0, y1, z0, u0, v0)
        self.__tessellator.addVertexWithUV(x0, y0, z0, u0, v1)
        self.__tessellator.addVertexWithUV(x0, y0, z1, u1, v1)

    cdef __renderBlockEast(self, Block block, int x, int y, int z, int tex):
        cdef int xt
        cdef float u0, u1, v0, v1, x1, y0, y1, z0, z1

        if self.__overrideBlockTexture >= 0:
            tex = self.__overrideBlockTexture

        xt = (tex & 15) << 4
        tex &= 240
        u0 = xt / 256.0
        u1 = (xt + 15.99) / 256.0
        v0 = 0.0
        v1 = 0.0
        if block.minY >= 0.0 and block.maxY <= 1.0:
            v0 = (tex + block.minY * 15.99) / 256.0
            v1 = (tex + block.maxY * 15.99) / 256.0
        else:
            v0 = tex / 256.0
            v1 = (tex + 15.99) / 256.0

        x1 = x + block.maxX
        y0 = y + block.minY
        y1 = y + block.maxY
        z0 = z + block.minZ
        z1 = z + block.maxZ
        self.__tessellator.addVertexWithUV(x1, y0, z1, u0, v1)
        self.__tessellator.addVertexWithUV(x1, y0, z0, u1, v1)
        self.__tessellator.addVertexWithUV(x1, y1, z0, u1, v0)
        self.__tessellator.addVertexWithUV(x1, y1, z1, u0, v0)

    def renderBlockOnInventory(self, Block block):
        cdef int renderType = block.getRenderType()
        if renderType == 0:
            gl.glTranslatef(-0.5, -0.5, -0.5)
            self.__tessellator.startDrawingQuads()
            self.__tessellator.setNormal(0.0, -1.0, 0.0)
            self.__renderBlockBottom(block, 0.0, 0.0, 0.0, block.getBlockTexture(0))
            self.__tessellator.draw()
            self.__tessellator.startDrawingQuads()
            self.__tessellator.setNormal(0.0, 1.0, 0.0)
            self.__renderBlockTop(block, 0.0, 0.0, 0.0, block.getBlockTexture(1))
            self.__tessellator.draw()
            self.__tessellator.startDrawingQuads()
            self.__tessellator.setNormal(0.0, 0.0, -1.0)
            self.__renderBlockNorth(block, 0, 0, 0, block.getBlockTexture(2))
            self.__tessellator.draw()
            self.__tessellator.startDrawingQuads()
            self.__tessellator.setNormal(0.0, 0.0, 1.0)
            self.__renderBlockSouth(block, 0, 0, 0, block.getBlockTexture(3))
            self.__tessellator.draw()
            self.__tessellator.startDrawingQuads()
            self.__tessellator.setNormal(-1.0, 0.0, 0.0)
            self.__renderBlockWest(block, 0, 0, 0, block.getBlockTexture(4))
            self.__tessellator.draw()
            self.__tessellator.startDrawingQuads()
            self.__tessellator.setNormal(1.0, 0.0, 0.0)
            self.__renderBlockEast(block, 0, 0, 0, block.getBlockTexture(5))
            self.__tessellator.draw()
            gl.glTranslatef(0.5, 0.5, 0.5)
        elif renderType == 1:
            self.__tessellator.startDrawingQuads()
            self.__tessellator.setNormal(0.0, -1.0, 0.0)
            self.__renderBlockPlant(block, -0.5, -0.5, -0.5)
            self.__tessellator.draw()
        elif renderType == 2:
            self.__tessellator.startDrawingQuads()
            self.__tessellator.setNormal(0.0, -1.0, 0.0)
            self.__renderBlockTorch(block, -0.5, -0.5, -0.5, 0.0, 0.0)
            self.__tessellator.draw()
