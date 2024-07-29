from mc.net.minecraft.client.gui.GuiLoadLevel import GuiLoadLevel
from mc.net.minecraft.client.gui.GuiNameLevel import GuiNameLevel
from mc.net.minecraft.client.PlayerLoader import PlayerLoader

import traceback

class GuiSaveLevel(GuiLoadLevel):

    def __init__(self, screen):
        super().__init__(screen)
        self._title = 'Save level'

    def initGui(self):
        super().initGui()
        self._controlList[5].displayString = 'Save file...'

    def _setLevels(self, levels):
        for i in range(5):
            self._controlList[i].displayString = levels[i]
            self._controlList[i].visible = True

        self._controlList[5].visible = True

    def _openFile(self, file):
        try:
            PlayerLoader(self.mc, self.mc.loadingScreen).save(self.mc.theWorld, file)
        except Exception as e:
            print(traceback.format_exc())

    def _openLevel(self, i):
        self.mc.displayGuiScreen(GuiNameLevel(self, self._controlList[i].displayString, i))
