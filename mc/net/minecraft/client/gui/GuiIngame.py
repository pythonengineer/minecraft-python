from mc.net.minecraft.client.controller.PlayerControllerSP import PlayerControllerSP
from mc.net.minecraft.client.render.RenderBlocks import RenderBlocks
from mc.net.minecraft.client.render.Tessellator import tessellator
from mc.net.minecraft.client.gui.Gui import Gui
from mc.net.minecraft.client.RenderHelper import RenderHelper
from mc.net.minecraft.client.ChatLine import ChatLine
from mc.net.minecraft.game.level.block.Blocks import blocks
from pyglet import window, gl
from random import Random
import math

class GuiIngame(Gui):
    __rand = Random()

    def __init__(self, minecraft, width, height):
        self.__mc = minecraft
        self.__ingameWidth = width * 240 // height
        self.__ingameHeight = height * 240 // height
        self.__blockRenderer = RenderBlocks(tessellator)
        self.chatMessageList = []
        self.updateCounter = 0

    def renderGameOverlay(self, scale):
        self.__mc.entityRenderer.setupOverlayRendering()
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.__mc.renderEngine.getTexture('gui/gui.png'))
        t = tessellator
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        gl.glEnable(gl.GL_BLEND)
        self._zLevel = -90.0
        self.drawTexturedModal(self.__ingameWidth / 2 - 91, self.__ingameHeight - 22, 0, 0, 182, 22)
        self.drawTexturedModal(self.__ingameWidth / 2 - 91 - 1 + self.__mc.thePlayer.inventory.currentItem * 20,
                               self.__ingameHeight - 22 - 1, 0, 22, 24, 22)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.__mc.renderEngine.getTexture('gui/icons.png'))
        self.drawTexturedModal(self.__ingameWidth / 2 - 7, self.__ingameHeight / 2 - 7, 0, 0, 16, 16)
        invulnerable = 1 if self.__mc.thePlayer.scoreValue // 3 % 2 == 1 else 0
        if self.__mc.thePlayer.scoreValue < 10:
            invulnerable = 0

        health = self.__mc.thePlayer.health
        prevHealth = self.__mc.thePlayer.prevHealth
        self.__rand.seed(self.updateCounter * 312871)
        if self.__mc.playerController.shouldDrawHUD():
            for i in range(10):
                n5 = 0
                if invulnerable != 0:
                    n5 = 1

                n4 = self.__ingameWidth / 2 - 91 + (i << 3)
                n3 = self.__ingameHeight - 32
                if health <= 4:
                    n3 += self.__rand.randint(0, 1)

                self.drawTexturedModal(n4, n3, 16 + n5 * 9, 0, 9, 9)
                if invulnerable != 0:
                    if (i << 1) + 1 < prevHealth:
                        self.drawTexturedModal(n4, n3, 70, 0, 9, 9)
                    elif (i << 1) + 1 == prevHealth:
                        self.drawTexturedModal(n4, n3, 79, 0, 9, 9)

                if (i << 1) + 1 < health:
                    self.drawTexturedModal(n4, n3, 52, 0, 9, 9)
                elif (i << 1) + 1 == health:
                    self.drawTexturedModal(n4, n3, 61, 0, 9, 9)

            if self.__mc.thePlayer.isInsideOfMaterial():
                n6 = math.ceil((self.__mc.thePlayer.air - 2) * 10.0 / 300.0)
                n5 = math.ceil(self.__mc.thePlayer.air * 10.0 / 300.0) - n6
                for n4 in range(n6 + n5):
                    if n4 < n6:
                        self.drawTexturedModal(self.__ingameWidth / 2 - 91 + (n4 << 3),
                                               self.__ingameHeight - 32 - 9, 16, 18, 9, 9)
                    else:
                        self.drawTexturedModal(self.__ingameWidth / 2 - 91 + (n4 << 3),
                                               self.__ingameHeight - 32 - 9, 25, 18, 9, 9)

        gl.glDisable(gl.GL_BLEND)
        gl.glEnable(gl.GL_NORMALIZE)
        gl.glPushMatrix()
        gl.glRotatef(180.0, 1.0, 0.0, 0.0)
        RenderHelper.enableStandardItemLighting()
        gl.glPopMatrix()

        for slot in range(len(self.__mc.thePlayer.inventory.mainInventory)):
            width = self.__ingameWidth // 2 - 90 + slot * 20
            height = self.__ingameHeight - 16
            block = self.__mc.thePlayer.inventory.mainInventory[slot]
            if block <= 0:
                continue

            gl.glPushMatrix()
            gl.glTranslatef(width, height, -50.0)
            if self.__mc.thePlayer.inventory.animationsToGo[slot] > 0:
                f2 = (self.__mc.thePlayer.inventory.animationsToGo[slot] - scale) / 5.0
                f3 = -(math.sin((f2 * f2) * math.pi)) * 8.0
                f4 = math.sin((f2 * f2) * math.pi) + 1.0
                f5 = math.sin(f2 * math.pi) + 1.0
                gl.glTranslatef(10.0, f3 + 10.0, 0.0)
                gl.glScalef(f4, f5, 1.0)
                gl.glTranslatef(-10.0, -10.0, 0.0)

            gl.glScalef(10.0, 10.0, 10.0)
            gl.glTranslatef(1.0, 0.5, 0.0)
            gl.glRotatef(210.0, 1.0, 0.0, 0.0)
            gl.glRotatef(45.0, 0.0, 1.0, 0.0)
            tex = self.__mc.renderEngine.getTexture('terrain.png')
            gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
            self.__blockRenderer.renderBlockOnInventory(blocks.blocksList[block])
            gl.glPopMatrix()
            if self.__mc.thePlayer.inventory.stackSize[slot] > 1:
                string = '' + str(self.__mc.thePlayer.inventory.stackSize[slot])
                self.__mc.fontRenderer.drawStringWithShadow(
                    string, width + 19 - self.__mc.fontRenderer.getWidth(string),
                    height + 6, 0xFFFFFF
                )

        RenderHelper.disableStandardItemLighting()
        gl.glDisable(gl.GL_NORMALIZE)
        self.__mc.fontRenderer.drawStringWithShadow(self.__mc.VERSION_STRING, 2, 2, 0xFFFFFF)
        if self.__mc.options.showFPS:
            self.__mc.fontRenderer.drawStringWithShadow(self.__mc.debug, 2, 12, 0xFFFFFF)

        if isinstance(self.__mc.playerController, PlayerControllerSP):
            score = 'Score: &e' + str(self.__mc.thePlayer.getScore())
            self.__mc.fontRenderer.drawStringWithShadow(
                score, self.__ingameWidth - self.__mc.fontRenderer.getWidth(score) - 2,
                2, 16777215
            )
            self.__mc.fontRenderer.drawStringWithShadow(
                'Arrows: ' + str(self.__mc.thePlayer.getArrows),
                self.__ingameWidth // 2 + 8, self.__ingameHeight - 33, 16777215
            )

        for i, message in enumerate(self.chatMessageList):
            if i >= 10:
                break

            if message.updateCounter < 200:
                self.__mc.fontRenderer.drawStringWithShadow(
                    None, 2, self.__ingameHeight - 8 - i * 9 - 20, 0xFFFFFF
                )
