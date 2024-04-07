from mc.net.minecraft.client.gui.Gui import Gui
from pyglet import gl

class GuiButton(Gui):

    def __init__(self, id_, x, y, width, height=None, string=None):
        if height is None:
            string = width
            width = 200
            height = 20

        self.id = id_
        self.__width = width
        self.__height = 20
        self.__x = x
        self.__y = y
        self.displayString = string
        self.enabled = True
        self.visible = True

    def drawButton(self, mc, xMouse, yMouse):
        if not self.visible:
            return

        gl.glBindTexture(gl.GL_TEXTURE_2D, mc.renderEngine.getTexture('gui/gui.png'))
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        onButton = True if xMouse >= self.__x and yMouse >= self.__y and \
                     xMouse < self.__x + self.__width and \
                     yMouse < self.__y + self.__height else False
        adjust = 1
        if not self.enabled:
            adjust = 0
        elif onButton:
            adjust = 2

        self.drawTexturedModalRect(self.__x, self.__y, 0, 46 + adjust * 20,
                                   self.__width / 2, self.__height)
        self.drawTexturedModalRect(self.__x + self.__width / 2, self.__y,
                                   200 - self.__width / 2, 46 + adjust * 20,
                                   self.__width / 2, self.__height)
        if not self.enabled:
            self.drawCenteredString(mc.fontRenderer, self.displayString,
                                    self.__x + self.__width // 2,
                                    self.__y + (self.__height - 8) // 2, -6250336)
        elif onButton:
            self.drawCenteredString(mc.fontRenderer, self.displayString,
                                    self.__x + self.__width // 2,
                                    self.__y + (self.__height - 8) // 2, 0xFFFFA0)
        else:
            self.drawCenteredString(mc.fontRenderer, self.displayString,
                                    self.__x + self.__width // 2,
                                    self.__y + (self.__height - 8) // 2, 0xE0E0E0)

    def mousePressed(self, xm, ym):
        return self.enabled and xm >= self.__x and ym >= self.__y and \
               xm < self.__x + self.__width and ym < self.__y + self.__height
