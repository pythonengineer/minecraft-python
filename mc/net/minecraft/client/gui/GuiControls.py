from mc.net.minecraft.client.gui.GuiButtonSmall import GuiButtonSmall
from mc.net.minecraft.client.gui.GuiScreen import GuiScreen
from mc.net.minecraft.client.gui.GuiButton import GuiButton

class GuiControls(GuiScreen):
    __screenTitle = 'Controls'
    __buttonId = -1

    def __init__(self, screen, options):
        self.__parentScreen = screen
        self.__options = options

    def initGui(self, minecraft, width, height):
        super().initGui(minecraft, width, height)
        for i, binding in enumerate(self.__options.keyBindings):
            self._controlList.append(GuiButtonSmall(i, self.width // 2 - 155 + i % 2 * 160,
                                                    self.height // 6 + 24 * (i >> 1),
                                                    self.__options.setKeyBindingString(i)))

        self._controlList.append(GuiButton(200, self.width // 2 - 100,
                                           self.height // 6 + 168, 'Done'))

    def _actionPerformed(self, button):
        for i, binding in enumerate(self.__options.keyBindings):
            self._controlList[i].displayString = self.__options.setKeyBindingString(i)

        if button.id == 200:
            self._mc.displayGuiScreen(self.__parentScreen)
        else:
            self.__buttonId = button.id
            button.displayString = '> ' + self.__options.setKeyBindingString(button.id) + ' <'

    def _keyTyped(self, key, char, motion):
        if self.__buttonId >= 0 and key:
            self.__options.setKeyBinding(self.__buttonId, key)
            self._controlList[self.__buttonId].displayString = self.__options.setKeyBindingString(self.__buttonId)
            self.__buttonId = -1
        else:
            super()._keyTyped(key, char, motion)

    def drawScreen(self, xm, ym):
        self._drawGradientRect(0, 0, self.width, self.height, 1610941696, -1607454624)
        self.drawCenteredString(self._font, self.__screenTitle, self.width // 2, 20, 16777215)
        super().drawScreen(xm, ym)
