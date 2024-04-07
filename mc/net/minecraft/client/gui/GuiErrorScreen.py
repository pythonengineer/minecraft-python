from mc.net.minecraft.client.gui.GuiScreen import GuiScreen

class GuiErrorScreen(GuiScreen):

    def __init__(self, title, text):
        self.__title = title
        self.__text = text

    def initGui(self, minecraft, width, height):
        super().initGui(minecraft, width, height)

    def drawScreen(self, xm, ym):
        self._drawGradientRect(0, 0, self.width, self.height, -12574688, -11530224)
        self.drawCenteredString(self._font, self.__title, self.width // 2, 90, 0xFFFFFF)
        self.drawCenteredString(self._font, self.__text, self.width // 2, 110, 0xFFFFFF)
        super().drawScreen(xm, ym)

    def _keyTyped(self, key, char, motion):
        pass
