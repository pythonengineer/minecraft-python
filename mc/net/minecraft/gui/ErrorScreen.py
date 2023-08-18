from mc.net.minecraft.gui.Screen import Screen

class ErrorScreen(Screen):

    def __init__(self, title, desc):
        self.__title = title
        self.__desc = desc

    def init(self, minecraft, width, height):
        super().init(minecraft, width, height)

    def render(self, xm, ym):
        self._fillGradient(0, 0, self._width, self._height, -12574688, -11530224)
        self.drawCenteredString(self.__title, self._width // 2, 90, 0xFFFFFF)
        self.drawCenteredString(self.__desc, self._width // 2, 110, 0xFFFFFF)
        super().render(xm, ym)

    def _keyPressed(self, key, char, motion):
        pass
