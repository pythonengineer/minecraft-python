from mc.net.minecraft.client.gui.GuiLoadLevel import GuiLoadLevel
from mc.net.minecraft.client.gui.GuiSaveBase import GuiSaveBase

class GuiSaveLevel(GuiLoadLevel):

    def __init__(self, screen):
        super().__init__(screen)
        self._title = 'Save level'

    def initGui(self, minecraft, width, height):
        super().initGui(minecraft, width, height)
        self._controlList[5].displayString = 'Save file...'

    def _setLevels(self, levels):
        for i in range(5):
            self._controlList[i].displayString = levels[i]
            self._controlList[i].visible = True

    def _openLevel(self, i):
        self._mc.displayGuiScreen(GuiSaveBase(self, self._controlList[i].displayString, i))
