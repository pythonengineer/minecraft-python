from mc.net.minecraft.client.gui.GuiScreen import GuiScreen
from mc.net.minecraft.client.gui.GuiButton import GuiButton
from pyglet import window

class GuiNewLevel(GuiScreen):

    def __init__(self, screen):
        self.__prevGui = screen
        self.__worldType = ('Inland', 'Island', 'Floating', 'Flat')
        self.__worldShape = ('Square', 'Long', 'Deep')
        self.__worldSize = ('Small', 'Normal', 'Huge')
        self.__worldTheme = ('Normal', 'Hell')
        self.__selectedWorldType = 1
        self.__selectedWorldShape = 0
        self.__selectedWorldSize = 1
        self.__selectedWorldTheme = 0

    def initGui(self, minecraft, width, height):
        super().initGui(minecraft, width, height)
        self._controlList.clear()
        self._controlList.append(GuiButton(0, self.width // 2 - 100,
                                           self.height // 4, 'Type: '))
        self._controlList.append(GuiButton(1, self.width // 2 - 100,
                                           self.height // 4 + 24, 'Shape:'))
        self._controlList.append(GuiButton(2, self.width // 2 - 100,
                                           self.height // 4 + 48, 'Size: '))
        self._controlList.append(GuiButton(3, self.width // 2 - 100,
                                           self.height // 4 + 72, 'Theme: '))
        self._controlList.append(GuiButton(4, self.width // 2 - 100,
                                           self.height // 4 + 96 + 12, 'Create'))
        self._controlList.append(GuiButton(5, self.width // 2 - 100,
                                           self.height // 4 + 120 + 12, 'Cancel'))
        self.__worldOptions()

    def __worldOptions(self):
        self._controlList[0].displayString = 'Type: ' + self.__worldType[self.__selectedWorldType]
        self._controlList[1].displayString = 'Shape: ' + self.__worldShape[self.__selectedWorldShape]
        self._controlList[2].displayString = 'Size: ' + self.__worldSize[self.__selectedWorldSize]
        self._controlList[3].displayString = 'Theme: ' + self.__worldTheme[self.__selectedWorldTheme]

    def _actionPerformed(self, button):
        if button.id == 5:
            self._mc.displayGuiScreen(self.__prevGui)
        elif button.id == 4:
            self._mc.generateNewLevel(self.__selectedWorldSize, self.__selectedWorldShape,
                                      self.__selectedWorldType, self.__selectedWorldTheme)
            self._mc.displayGuiScreen(None)
            self._mc.setIngameFocus()
        elif button.id == 0:
            self.__selectedWorldType = (self.__selectedWorldType + 1) % len(self.__worldType)
        elif button.id == 1:
            self.__selectedWorldShape = (self.__selectedWorldShape + 1) % len(self.__worldShape)
        elif button.id == 2:
            self.__selectedWorldSize = (self.__selectedWorldSize + 1) % len(self.__worldSize)
        elif button.id == 3:
            self.__selectedWorldTheme = (self.__selectedWorldTheme + 1) % len(self.__worldTheme)

        self.__worldOptions()

    def drawScreen(self, xm, ym):
        self._drawGradientRect(0, 0, self.width, self.height, 1610941696, -1607454624)
        self.drawCenteredString(self._fontRenderer, 'Generate new level',
                                self.width // 2, 40, 0xFFFFFF)
        super().drawScreen(xm, ym)
