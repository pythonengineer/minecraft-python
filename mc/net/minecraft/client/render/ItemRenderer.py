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
            gl.glRotatef(swingX * 80.0, 0.0, 1.0, 0.0)
            gl.glRotatef(-swingY * 20.0, 1.0, 0.0, 0.0)

        brightness = self.__mc.theWorld.getBlockLightValue(int(self.__mc.thePlayer.posX),
                                                           int(self.__mc.thePlayer.posY),
                                                           int(self.__mc.thePlayer.posZ))
        gl.glColor4f(brightness, brightness, brightness, 1.0)
        item = self.__itemToRender
        if item:
            gl.glScalef(0.4, 0.4, 0.4)
            gl.glBindTexture(gl.GL_TEXTURE_2D, self.__mc.renderEngine.getTexture('terrain.png'))
            if item.itemID > 0:
                self.__renderBlocksInstance.renderBlockOnInventory(blocks.blocksList[item.itemID])
            else:
                gl.glBindTexture(gl.GL_TEXTURE_2D, self.__mc.renderEngine.getTexture('gui/items.png'))
                gl.glDisable(gl.GL_LIGHTING)
                t = tessellator
                u0 = (item.iconIndex % 16 << 4) / 256.0
                u1 = ((item.iconIndex % 16 << 4) + 16) / 256.0
                v0 = (item.iconIndex // 16 << 4) / 256.0
                v1 = ((item.iconIndex // 16 << 4) + 16) / 256.0
                t.startDrawingQuads()
                t.addVertexWithUV(-0.4, -0.2, -0.4, u0, v1)
                t.addVertexWithUV(0.29999998, -0.2, 0.29999998, u1, v1)
                t.addVertexWithUV(0.29999998, 0.8, 0.29999998, u1, v0)
                t.addVertexWithUV(-0.4, 0.8, -0.4, u0, v0)
                t.draw()
                gl.glEnable(gl.GL_LIGHTING)
        else:
            gl.glScalef(1.0, -1.0, -1.0)
            gl.glTranslatef(0.0, 0.2, 0.0)
            gl.glRotatef(-120.0, 0.0, 0.0, 1.0)
            gl.glScalef(1.0, 1.0, 1.0)

        gl.glDisable(gl.GL_NORMALIZE)
        gl.glPopMatrix()
        RenderHelper.disableStandardItemLighting()

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

    def equipAnimationSpeed(self):
        self.__equippedProgress = 0.0

    def equippedItemRender(self):
        self.__swingProgress = -1
        self.__itemSwingState = True
