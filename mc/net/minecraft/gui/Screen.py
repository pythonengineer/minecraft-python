from mc.net.minecraft.gui.Gui import Gui
from mc.net.minecraft.renderer.Tesselator import tesselator
from mc.CompatibilityShims import rshift
from pyglet import window, gl

class Screen(Gui):

    def render(self, xMouse, yMouse):
        for button in self._buttons:
            if button.visible:
                gl.glEnable(gl.GL_TEXTURE_2D)
                gl.glBindTexture(gl.GL_TEXTURE_2D, self._minecraft.textures.getTextureId('gui.png'))
                gl.glColor4f(1.0, 1.0, 1.0, 1.0)
                z6 = xMouse >= button.w and yMouse >= button.h and xMouse < button.w + button.x and yMouse < button.h + button.y
                b9 = 1
                if not button.enabled:
                    b9 = 0
                elif z6:
                    b9 = 2

                button.blit(button.w, button.h, 0, 46 + b9 * 20, button.x / 2, button.y)
                button.blit(button.w + button.x / 2, button.h, 200 - button.x / 2, 46 + b9 * 20, button.x / 2, button.y)
                if not button.enabled:
                    button.drawCenteredString(self._font, button.msg, button.w + button.x // 2, button.h + (button.y - 8) // 2, -6250336)
                elif z6:
                    button.drawCenteredString(self._font, button.msg, button.w + button.x // 2, button.h + (button.y - 8) // 2, 16777120)
                else:
                    button.drawCenteredString(self._font, button.msg, button.w + button.x // 2, button.h + (button.y - 8) // 2, 14737632)

    def _keyPressed(self, key, char, motion):
        if key == window.key.ESCAPE:
            self._minecraft.setScreen(None)
            self._minecraft.grabMouse()

    def _mousePressed(self, xm, ym, button):
        if button == window.mouse.LEFT:
            for button in self._buttons:
                if button.enabled and xm >= button.w and ym >= button.h and xm < button.w + button.x and ym < button.h + button.y:
                    self._buttonClicked(button)

    def _buttonClicked(self, button):
        pass

    def init(self, minecraft, width, height):
        self._minecraft = minecraft
        self._font = minecraft.font
        self._width = width
        self._height = height
        self._buttons = []
        self.allowUserInput = False

    def updateMouseEvents(self, button):
        xm = self._minecraft.mouseX * self._width // self._minecraft.width
        ym = self._height - self._minecraft.mouseY * self._height // self._minecraft.height - 1
        self._mousePressed(xm, ym, button)

    def updateKeyboardEvents(self, key=None, char=None, motion=None):
        self._keyPressed(key, char, motion)

    def tick(self):
        pass

    def closeScreen(self):
        pass
