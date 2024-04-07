from mc.net.minecraft.client.gui.GuiScreen import GuiScreen
from mc.net.minecraft.client.gui.GuiButton import GuiButton
from pyglet import window

class GuiNewLevel(GuiScreen):

    def __init__(self, screen):
        self.__parentScr = screen

    def initGui(self, minecraft, width, height):
        super().initGui(minecraft, width, height)
        self._controlList.clear()
        self._controlList.append(GuiButton(0, self.width // 2 - 100,
                                           self.height // 4, 'Small'))
        self._controlList.append(GuiButton(1, self.width // 2 - 100,
                                           self.height // 4 + 24, 'Normal'))
        self._controlList.append(GuiButton(2, self.width // 2 - 100,
                                           self.height // 4 + 48, 'Huge'))
        self._controlList.append(GuiButton(3, self.width // 2 - 100,
                                           self.height // 4 + 120, 'Cancel'))

    def _actionPerformed(self, button):
        if button.id == 3:
            self._mc.displayGuiScreen(self.__parentScr)
        else:
            self._mc.generateNewLevel(button.id)
            self._mc.displayGuiScreen(None)
            self._mc.setIngameFocus()

    def drawScreen(self, xm, ym):
        self._drawGradientRect(0, 0, self.width, self.height, 1610941696, -1607454624)
        self.drawCenteredString(self._font, 'Generate new level',
                                self.width // 2, 40, 0xFFFFFF)
        super().drawScreen(xm, ym)
