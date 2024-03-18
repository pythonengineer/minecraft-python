from mc.net.minecraft.client.render.Tessellator import tessellator
from mc.net.minecraft.client.render.RenderBlocks import RenderBlocks
from mc.net.minecraft.game.level.block.Blocks import blocks
from mc.net.minecraft.client.gui.GuiScreen import GuiScreen
from mc.net.minecraft.client.RenderHelper import RenderHelper
from mc.net.minecraft.client.Session import Session
from pyglet import window, gl

class GuiCreativeInventory(GuiScreen):

    def __init__(self):
        self.__blockRenderer = RenderBlocks(tessellator)
        self.allowUserInput = True

    def __getIsMouseOverSlot(self, x, y):
        for i in range(len(Session.allowedBlocks)):
            w = self._width // 2 + i % 9 * 24 + -108 - 3
            h = self._height // 2 + i // 9 * 24 + -60 + 3
            if x >= w and x <= w + 24 and y >= h - 12 and y <= h + 12:
                return i

        return -1

    def drawScreen(self, xm, ym):
        xm = self.__getIsMouseOverSlot(xm, ym)
        self._drawGradientRect(self._width // 2 - 120, 30, self._width // 2 + 120,
                               180, -1878719232, -1070583712)
        if xm >= 0:
            w = self._width // 2 + xm % 9 * 24 + -108
            h = self._height // 2 + xm // 9 * 24 + -60
            self._drawGradientRect(w - 3, h - 8, w + 23, h + 24 - 6, -1862270977, -1056964609)

        self.drawCenteredString(self._fontRenderer, 'Select block', self._width // 2, 40, 0xFFFFFF)
        t = tessellator
        tex = self._mc.renderEngine.getTexture('terrain.png')
        gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
        gl.glPushMatrix()
        gl.glRotatef(180.0, 1.0, 0.0, 0.0)
        RenderHelper.enableStandardItemLighting()
        gl.glPopMatrix()
        gl.glEnable(gl.GL_NORMALIZE)
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)

        for i in range(len(Session.allowedBlocks)):
            block = Session.allowedBlocks[i]
            gl.glPushMatrix()
            w = self._width // 2 + i % 9 * 24 + -108
            h = self._height // 2 + i // 9 * 24 + -60
            gl.glTranslatef(w, h, 0.0)
            gl.glScalef(10.0, 10.0, 10.0)
            gl.glTranslatef(1.0, 0.5, 8.0)
            gl.glRotatef(210.0, 1.0, 0.0, 0.0)
            gl.glRotatef(45.0, 0.0, 1.0, 0.0)
            if xm == i:
                gl.glScalef(1.6, 1.6, 1.6)

            self.__blockRenderer.renderBlockOnInventory(block)
            gl.glPopMatrix()

        gl.glDisable(gl.GL_NORMALIZE)
        RenderHelper.disableStandardItemLighting()

    def _mouseClicked(self, xm, ym, button):
        if button == window.mouse.LEFT:
            slot = self.__getIsMouseOverSlot(xm, ym)
            if slot >= 0:
                self._mc.thePlayer.inventory.replaceSlot(Session.allowedBlocks[slot])

            self._mc.displayGuiScreen(None)
