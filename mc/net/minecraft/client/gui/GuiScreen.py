from mc.net.minecraft.client.gui.Gui import Gui
from mc.net.minecraft.client.render.Tessellator import tessellator
from pyglet import window, gl

class GuiScreen(Gui):
    allowUserInput = False

    def drawScreen(self, xMouse, yMouse):
        for button in self._controlList:
            button.drawButton(self._mc, xMouse, yMouse)

    def _keyTyped(self, key, char, motion):
        if key == window.key.ESCAPE:
            self._mc.displayGuiScreen(None)
            self._mc.setIngameFocus()

    def _mouseClicked(self, xm, ym, button):
        if button == window.mouse.LEFT:
            for button in self._controlList:
                if button.mousePressed(xm, ym):
                    self._mc.sndManager.playSound('random.click', 1.0, 1.0)
                    self._actionPerformed(button)

    def _actionPerformed(self, button):
        pass

    def initGui(self, minecraft, width, height):
        self._mc = minecraft
        self._font = minecraft.fontRenderer
        self.width = width
        self.height = height
        self._controlList = []

    def handleMouseInput(self, button):
        xm = self._mc.mouseX * self.width // self._mc.width
        ym = self.height - self._mc.mouseY * self.height // self._mc.height - 1
        self._mouseClicked(xm, ym, button)

    def handleKeyboardEvent(self, key=None, char=None, motion=None):
        self._keyTyped(key, char, motion)

    def updateScreen(self):
        pass

    def onGuiClose(self):
        pass
