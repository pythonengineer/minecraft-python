from mc.net.minecraft.client.gui.Gui import Gui
from mc.net.minecraft.client.render.Tessellator import tessellator
from pyglet import window, gl

class GuiScreen(Gui):
    allowUserInput = False

    def drawScreen(self, xMouse, yMouse):
        for button in self._controlList:
            if not button.visible:
                continue

            gl.glBindTexture(gl.GL_TEXTURE_2D, self._mc.renderEngine.getTexture('gui/gui.png'))
            gl.glColor4f(1.0, 1.0, 1.0, 1.0)
            z6 = True if xMouse >= button.x and yMouse >= button.y and \
                         xMouse < button.x + button.width and \
                         yMouse < button.y + button.height else False
            b9 = 1
            if not button.enabled:
                b9 = 0
            elif z6:
                b9 = 2

            button.drawTexturedModal(button.x, button.y, 0, 46 + b9 * 20,
                                     button.width / 2, button.height)
            button.drawTexturedModal(button.x + button.width / 2, button.y,
                                     200 - button.width / 2, 46 + b9 * 20,
                                     button.width / 2, button.height)
            if not button.enabled:
                button.drawCenteredString(self._fontRenderer, button.displayString,
                                          button.x + button.width // 2,
                                          button.y + (button.height - 8) // 2, -6250336)
            elif z6:
                button.drawCenteredString(self._fontRenderer, button.displayString,
                                          button.x + button.width // 2,
                                          button.y + (button.height - 8) // 2, 0xFFFFA0)
            else:
                button.drawCenteredString(self._fontRenderer, button.displayString,
                                          button.x + button.width // 2,
                                          button.y + (button.height - 8) // 2, 0xE0E0E0)

    def _keyTyped(self, key, char, motion):
        if key == window.key.ESCAPE:
            self._mc.displayGuiScreen(None)
            self._mc.setIngameFocus()

    def _mouseClicked(self, xm, ym, button):
        if button == window.mouse.LEFT:
            for button in self._controlList:
                if button.enabled and xm >= button.x and ym >= button.y and \
                   xm < button.x + button.width and ym < button.y + button.height:
                    self._actionPerformed(button)

    def _actionPerformed(self, button):
        pass

    def initGui(self, minecraft, width, height):
        self._mc = minecraft
        self._fontRenderer = minecraft.fontRenderer
        self._width = width
        self._height = height
        self._controlList = []

    def handleMouseInput(self, button):
        xm = self._mc.mouseX * self._width // self._mc.width
        ym = self._height - self._mc.mouseY * self._height // self._mc.height - 1
        self._mouseClicked(xm, ym, button)

    def handleKeyboardEvent(self, key=None, char=None, motion=None):
        self._keyTyped(key, char, motion)

    def updateScreen(self):
        pass

    def onClose(self):
        pass
