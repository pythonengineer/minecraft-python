from mc.net.minecraft.client.gui.GuiScreen import GuiScreen
from mc.net.minecraft.client.gui.GuiOptions import GuiOptions
from mc.net.minecraft.client.gui.GuiNewLevel import GuiNewLevel
from mc.net.minecraft.client.gui.GuiLoadLevel import GuiLoadLevel
from mc.net.minecraft.client.gui.GuiButton import GuiButton
from mc.net.minecraft.client.render.Tessellator import tessellator
from mc.JavaUtils import getMillis
from pyglet import gl

import math

class GuiMainTitle(GuiScreen):

    def __init__(self):
        self.__updateCounter = 0.0

    def updateScreen(self):
        self.__updateCounter += 0.01

    def _keyTyped(self, key, char, motion):
        pass

    def initGui(self):
        self._controlList.clear()
        self._controlList.append(GuiButton(1, self.width // 2 - 100,
                                           self.height // 4 + 48, 'Generate new level...'))
        self._controlList.append(GuiButton(2, self.width // 2 - 100,
                                           self.height // 4 + 72, 'Load level..'))
        self._controlList.append(GuiButton(3, self.width // 2 - 100,
                                           self.height // 4 + 96, 'Play tutorial level'))
        self._controlList.append(GuiButton(0, self.width // 2 - 100,
                                           self.height // 4 + 120 + 12, 'Options...'))
        self._controlList[2].enabled = False
        if not self.mc.session:
            self._controlList[1].enabled = False

    def _actionPerformed(self, button):
        if button.id == 0:
            self.mc.displayGuiScreen(GuiOptions(self, self.mc.options))
        elif button.id == 1:
            self.mc.displayGuiScreen(GuiNewLevel(self))
        elif self.mc.session and button.id == 2:
            self.mc.displayGuiScreen(GuiLoadLevel(self))

    def drawScreen(self, xm, ym):
        gl.glDisable(gl.GL_LIGHTING)
        gl.glDisable(gl.GL_FOG)
        t = tessellator
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.mc.renderEngine.getTexture('dirt.png'))
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        t.startDrawingQuads()
        t.setColorOpaque_I(4210752)
        t.addVertexWithUV(0.0, self.height, 0.0, 0.0,
                          self.height / 32.0 + self.__updateCounter)
        t.addVertexWithUV(self.width, self.height, 0.0, self.width / 32.0,
                          self.height / 32.0 + self.__updateCounter)
        t.addVertexWithUV(self.width, 0.0, 0.0,
                          self.width / 32.0, 0.0 + self.__updateCounter)
        t.addVertexWithUV(0.0, 0.0, 0.0, 0.0, 0.0 + self.__updateCounter)
        t.draw()
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.mc.renderEngine.getTexture('gui/logo.png'))
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        t.setColorOpaque_I(16777215)
        self.drawTexturedModalRect((self.width - 256) // 2, 30, 0, 0, 256, 49)
        gl.glPushMatrix()
        gl.glTranslatef(self.width / 2 + 90, 70.0, 0.0)
        gl.glRotatef(-20.0, 0.0, 0.0, 1.0)
        size = 1.8 - abs(math.sin((getMillis() % 1000) / 1000.0 * math.pi * 2.0) * 0.1)
        gl.glScalef(size, size, size)
        self.drawCenteredString(self._fontRenderer, 'Pre-beta!', 0, -8, 16776960)
        gl.glPopMatrix()
        copyright = 'Copyright Mojang Specifications. Do not distribute.'
        self.drawString(
            self._fontRenderer, copyright,
            self.width - self._fontRenderer.getStringWidth(copyright) - 2,
            self.height - 10, 16777215
        )
        super().drawScreen(xm, ym)
