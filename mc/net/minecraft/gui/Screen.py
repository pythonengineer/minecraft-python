from mc.net.minecraft.gui.GuiComponent import GuiComponent
from mc.net.minecraft.renderer.Tesselator import tesselator
from mc.CompatibilityShims import rshift
from pyglet import window, gl

class Screen(GuiComponent):
    allowUserInput = False

    def render(self, xMouse, yMouse):
        for button in self._buttons:
            if not button.visible:
                continue

            gl.glBindTexture(gl.GL_TEXTURE_2D, self._minecraft.textures.loadTexture('gui/gui.png'))
            gl.glColor4f(1.0, 1.0, 1.0, 1.0)
            z6 = True if xMouse >= button.x and yMouse >= button.y and xMouse < button.x + button.w and yMouse < button.y + button.h else False
            b9 = 1
            if not button.enabled:
                b9 = 0
            elif z6:
                b9 = 2

            button.blit(button.x, button.y, 0, 46 + b9 * 20, button.w / 2, button.h)
            button.blit(button.x + button.w / 2, button.y, 200 - button.w / 2, 46 + b9 * 20, button.w / 2, button.h)
            if not button.enabled:
                button.drawCenteredString(self._font, button.msg, button.x + button.w // 2, button.y + (button.h - 8) // 2, -6250336)
                continue

            if z6:
                button.drawCenteredString(self._font, button.msg, button.x + button.w // 2, button.y + (button.h - 8) // 2, 0xFFFFA0)
                continue

            button.drawCenteredString(self._font, button.msg, button.x + button.w // 2, button.y + (button.h - 8) // 2, 0xE0E0E0)

    def _keyPressed(self, key, char, motion):
        if key == window.key.ESCAPE:
            self._minecraft.setScreen(None)
            self._minecraft.grabMouse()

    def _mouseClicked(self, xm, ym, button):
        if button == window.mouse.LEFT:
            for button in self._buttons:
                if button.enabled and xm >= button.x and ym >= button.y and xm < button.x + button.w and ym < button.y + button.h:
                    self._buttonClicked(button)

    def _buttonClicked(self, button):
        pass

    def init(self, minecraft, width, height):
        self._minecraft = minecraft
        self._font = minecraft.font
        self._width = width
        self._height = height
        self._buttons = []

    def mouseEvent(self, button):
        xm = self._minecraft.mouseX * self._width // self._minecraft.width
        ym = self._height - self._minecraft.mouseY * self._height // self._minecraft.height - 1
        self._mouseClicked(xm, ym, button)

    def keyboardEvent(self, key=None, char=None, motion=None):
        self._keyPressed(key, char, motion)

    def tick(self):
        pass

    def removed(self):
        pass
