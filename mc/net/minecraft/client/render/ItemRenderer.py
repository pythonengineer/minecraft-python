from mc.net.minecraft.client.render.RenderBlocks import RenderBlocks
from mc.net.minecraft.client.render.Tessellator import tessellator
from mc.net.minecraft.client.RenderHelper import RenderHelper
from mc.net.minecraft.game.level.block.Blocks import blocks
from pyglet import gl

import math

class ItemRenderer:

    def __init__(self, minecraft):
        self.__mc = minecraft
        self.__itemToRender = None
        self.__equippedProgress = 0.0
        self.__prevEquippedProgress = 0.0
        self.__swingProgress = 0
        self.__itemSwingState = False
        self.__renderBlocksInstance = RenderBlocks(tessellator)

    def renderItemInFirstPerson(self, alpha):
        progress = self.__prevEquippedProgress + (self.__equippedProgress - self.__prevEquippedProgress) * alpha
        gl.glPushMatrix()
        gl.glRotatef(
            self.__mc.thePlayer.prevRotationPitch + (self.__mc.thePlayer.rotationPitch - self.__mc.thePlayer.prevRotationPitch) * alpha,
            1.0, 0.0, 0.0
        )
        gl.glRotatef(
            self.__mc.thePlayer.prevRotationYaw + (self.__mc.thePlayer.rotationYaw - self.__mc.thePlayer.prevRotationYaw) * alpha,
            0.0, 1.0, 0.0
        )
        RenderHelper.enableStandardItemLighting()
        gl.glPopMatrix()
        gl.glPushMatrix()
        if self.__itemSwingState:
            slot = (self.__swingProgress + alpha) / 8.0
            swingY = math.sin(slot * math.pi)
            swingX = math.sin(math.sqrt(slot) * math.pi)
            gl.glTranslatef(-swingX * 0.4,
                            math.sin(math.sqrt(slot) * math.pi * 2.0) * 0.2,
                            -swingY * 0.2)

        gl.glTranslatef(0.56, -0.52 - (1.0 - progress) * 0.6, -0.71999997)
        gl.glRotatef(45.0, 0.0, 1.0, 0.0)
        gl.glEnable(gl.GL_NORMALIZE)
        if self.__itemSwingState:
            slot = (self.__swingProgress + alpha) / 8.0
            swingY = math.sin((slot * slot) * math.pi)
            swingX = math.sin(math.sqrt(slot) * math.pi)
            gl.glRotatef(-swingY * 20.0, 0.0, 1.0, 0.0)
            gl.glRotatef(-swingX * 20.0, 0.0, 0.0, 1.0)
            gl.glRotatef(-swingX * 80.0, 1.0, 0.0, 0.0)

        brightness = self.__mc.theWorld.getBlockLightValue(int(self.__mc.thePlayer.posX),
                                                           int(self.__mc.thePlayer.posY),
                                                           int(self.__mc.thePlayer.posZ))
        gl.glColor4f(brightness, brightness, brightness, 1.0)
        if self.__itemToRender:
            gl.glScalef(0.4, 0.4, 0.4)
            gl.glBindTexture(gl.GL_TEXTURE_2D,
                             self.__mc.renderEngine.getTexture('terrain.png'))
            if self.__itemToRender.itemID < 256 and \
               blocks.blocksList[self.__itemToRender.itemID].getRenderType() == 0:
                self.__renderBlocksInstance.renderBlockOnInventory(
                    blocks.blocksList[self.__itemToRender.itemID]
                )
            else:
                if self.__itemToRender.itemID < 256:
                    gl.glBindTexture(gl.GL_TEXTURE_2D, self.__mc.renderEngine.getTexture('terrain.png'))
                else:
                    gl.glBindTexture(gl.GL_TEXTURE_2D, self.__mc.renderEngine.getTexture('gui/items.png'))

                t = tessellator
                u0 = (self.__itemToRender.getItem().getIconIndex() % 16 << 4) / 256.0
                u1 = ((self.__itemToRender.getItem().getIconIndex() % 16 << 4) + 16) / 256.0
                v0 = (self.__itemToRender.getItem().getIconIndex() // 16 << 4) / 256.0
                v1 = ((self.__itemToRender.getItem().getIconIndex() // 16 << 4) + 16) / 256.0
                gl.glEnable(gl.GL_NORMALIZE)
                gl.glTranslatef(0.0, -0.3, 0.0)
                gl.glScalef(1.5, 1.5, 1.5)
                gl.glRotatef(50.0, 0.0, 1.0, 0.0)
                gl.glRotatef(335.0, 0.0, 0.0, 1.0)
                gl.glTranslatef(-(15.0 / 16.0), -(1.0 / 16.0), 0.0)
                t.setNormal(0.0, 0.0, 1.0)
                t.startDrawingQuads()
                t.addVertexWithUV(0.0, 0.0, 0.0, u1, v1)
                t.addVertexWithUV(1.0, 0.0, 0.0, u0, v1)
                t.addVertexWithUV(1.0, 1.0, 0.0, u0, v0)
                t.addVertexWithUV(0.0, 1.0, 0.0, u1, v0)
                t.draw()
                t.setNormal(0.0, 0.0, -1.0)
                t.startDrawingQuads()
                t.addVertexWithUV(0.0, 1.0, -(1.0 / 16.0), u1, v0)
                t.addVertexWithUV(1.0, 1.0, -(1.0 / 16.0), u0, v0)
                t.addVertexWithUV(1.0, 0.0, -(1.0 / 16.0), u0, v1)
                t.addVertexWithUV(0.0, 0.0, -(1.0 / 16.0), u1, v1)
                t.draw()
                t.setNormal(-1.0, 0.0, 0.0)
                t.startDrawingQuads()
                for i in range(16):
                    x = i / 16.0
                    u = u1 + (u0 - u1) * x - 0.001953125
                    x *= 1.0
                    t.addVertexWithUV(x, 0.0, -(1.0 / 16.0), u, v1)
                    t.addVertexWithUV(x, 0.0, 0.0, u, v1)
                    t.addVertexWithUV(x, 1.0, 0.0, u, v0)
                    t.addVertexWithUV(x, 1.0, -(1.0 / 16.0), u, v0)

                t.draw()
                t.setNormal(1.0, 0.0, 0.0)
                t.startDrawingQuads()
                for i in range(16):
                    x = i / 16.0
                    u = u1 + (u0 - u1) * x - 0.001953125
                    x = x * 1.0 + 1.0 / 16.0
                    t.addVertexWithUV(x, 1.0, -(1.0 / 16.0), u, v0)
                    t.addVertexWithUV(x, 1.0, 0.0, u, v0)
                    t.addVertexWithUV(x, 0.0, 0.0, u, v1)
                    t.addVertexWithUV(x, 0.0, -(1.0 / 16.0), u, v1)

                t.draw()
                t.setNormal(0.0, 1.0, 0.0)
                t.startDrawingQuads()
                for i in range(16):
                    y = i / 16.0
                    v = v1 + (v0 - v1) * y - 0.001953125
                    y = y * 1.0 + 1.0 / 16.0
                    t.addVertexWithUV(0.0, y, 0.0, u1, v)
                    t.addVertexWithUV(1.0, y, 0.0, u0, v)
                    t.addVertexWithUV(1.0, y, -(1.0 / 16.0), u0, v)
                    t.addVertexWithUV(0.0, y, -(1.0 / 16.0), u1, v)

                t.draw()
                t.setNormal(0.0, -1.0, 0.0)
                t.startDrawingQuads()
                for i in range(16):
                    y = i / 16.0
                    v = v1 + (v0 - v1) * y - 0.001953125
                    y *= 1.0
                    t.addVertexWithUV(1.0, y, 0.0, u0, v)
                    t.addVertexWithUV(0.0, y, 0.0, u1, v)
                    t.addVertexWithUV(0.0, y, -(1.0 / 16.0), u1, v)
                    t.addVertexWithUV(1.0, y, -(1.0 / 16.0), u0, v)

                t.draw()
                gl.glDisable(gl.GL_NORMALIZE)
        else:
            gl.glScalef(1.0, -1.0, -1.0)
            gl.glTranslatef(0.0, 0.2, 0.0)
            gl.glRotatef(-120.0, 0.0, 0.0, 1.0)
            gl.glScalef(1.0, 1.0, 1.0)

        gl.glDisable(gl.GL_NORMALIZE)
        gl.glPopMatrix()
        RenderHelper.disableStandardItemLighting()

    def renderInMaterial(self, alpha):
        if self.__mc.thePlayer.fire > 0:
            tex = self.__mc.renderEngine.getTexture('terrain.png')
            gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
            t = tessellator
            gl.glColor4f(1.0, 1.0, 1.0, 0.9)
            gl.glEnable(gl.GL_BLEND)
            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
            for i in range(2):
                gl.glPushMatrix()
                tex = blocks.fire.blockIndexInTexture + (i << 4)
                xt = (tex & 15) << 4
                tex &= 240
                u0 = xt / 256.0
                u1 = (xt + 15.99) / 256.0
                v0 = tex / 256.0
                v1 = (tex + 15.99) / 256.0
                gl.glTranslatef(-((i << 1) - 1) * 0.24, -0.3, 0.0)
                gl.glRotatef(((i << 1) - 1) * 10.0, 0.0, 1.0, 0.0)
                t.startDrawingQuads()
                t.addVertexWithUV(-0.5, -0.5, -0.5, u1, v1)
                t.addVertexWithUV(0.5, -0.5, -0.5, u0, v1)
                t.addVertexWithUV(0.5, 0.5, -0.5, u0, v0)
                t.addVertexWithUV(-0.5, 0.5, -0.5, u1, v0)
                t.draw()
                gl.glPopMatrix()

            gl.glColor4f(1.0, 1.0, 1.0, 1.0)
            gl.glDisable(gl.GL_BLEND)
        if self.__mc.thePlayer.isInsideOfMaterial():
            tex = self.__mc.renderEngine.getTexture('water.png')
            gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
            t = tessellator
            br = self.__mc.thePlayer.getBrightness(alpha)
            gl.glColor4f(br, br, br, 0.5)
            gl.glEnable(gl.GL_BLEND)
            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
            gl.glPushMatrix()
            t.startDrawingQuads()
            t.addVertexWithUV(-1.0, -1.0, -0.5, 4.0, 4.0)
            t.addVertexWithUV(1.0, -1.0, -0.5, 0.0, 4.0)
            t.addVertexWithUV(1.0, 1.0, -0.5, 0.0, 0.0)
            t.addVertexWithUV(-1.0, 1.0, -0.5, 4.0, 0.0)
            t.draw()
            gl.glPopMatrix()
            gl.glColor4f(1.0, 1.0, 1.0, 1.0)
            gl.glDisable(gl.GL_BLEND)

    def updateEquippedItem(self):
        self.__prevEquippedProgress = self.__equippedProgress
        if self.__itemSwingState:
            self.__swingProgress += 1
            if self.__swingProgress == 8:
                self.__swingProgress = 0
                self.__itemSwingState = False

        block = self.__mc.thePlayer.inventory.getCurrentItem()
        progress = 1.0 if block == self.__itemToRender else 0.0
        progress -= self.__equippedProgress
        if progress < -0.4:
            progress = -0.4
        elif progress > 0.4:
            progress = 0.4

        self.__equippedProgress += progress
        if self.__equippedProgress < 0.1:
            self.__itemToRender = block

    def resetEquippedProgress(self):
        self.__equippedProgress = 0.0

    def swingItem(self):
        self.__swingProgress = -1
        self.__itemSwingState = True
