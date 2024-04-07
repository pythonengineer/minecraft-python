from mc.net.minecraft.client.gui.GuiScreen import GuiScreen
from mc.net.minecraft.client.gui.GuiButton import GuiButton

class GuiLoadLevel(GuiScreen):

    def __init__(self, screen):
        self.__parent = screen
        self.__finished = False
        self.__loaded = False
        self.__levels = []
        self.__status = ''
        self._title = 'Load level'

    def _setLevels(self, levels):
        for i in range(5):
            self._controlList[i].enabled = levels[i] != '-'
            self._controlList[i].displayString = levels[i]
            self._controlList[i].visible = True

    def initGui(self, minecraft, width, height):
        super().initGui(minecraft, width, height)

        for i in range(5):
            self._controlList.append(GuiButton(i, self.width // 2 - 100,
                                               self.height // 6 + i * 24, '---'))
            self._controlList[i].visible = False

        self._controlList.append(GuiButton(5, self.width // 2 - 100,
                                           self.height // 6 + 120 + 12, 'Load file...'))
        self._controlList.append(GuiButton(6, self.width // 2 - 100,
                                           self.height // 6 + 168, 'Cancel'))
        self._controlList[5].visible = False

        self._setLevels(['-', '-', '-', '-', '-'])
        self.__loaded = True

    def _actionPerformed(self, button):
        if not button.enabled:
            return

        if self.__loaded and button.id < 5:
            self._openLevel(button.id)
        elif self.__finished or self.__loaded and button.id == 6:
            self._mc.displayGuiScreen(self.__parent)

    def _openLevel(self, id_):
        self._mc.displayGuiScreen(None)
        self._mc.setIngameFocus()

    def drawScreen(self, xm, ym):
        self._drawGradientRect(0, 0, self.width, self.height, 1610941696, -1607454624)
        self.drawCenteredString(self._font, self._title, self.width // 2, 20, 0xFFFFFF)
        if not self.__loaded:
            self.drawCenteredString(self._font, self.__status, self.width // 2, self.height // 2 - 4, 0xFFFFFF)

        super().drawScreen(xm, ym)
