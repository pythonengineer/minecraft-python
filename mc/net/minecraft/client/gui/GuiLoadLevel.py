from mc.net.minecraft.client.gui.GuiLevelDialog import GuiLevelDialog
from mc.net.minecraft.client.gui.GuiScreen import GuiScreen
from mc.net.minecraft.client.gui.GuiButton import GuiButton
from mc.net.minecraft.client.PlayerLoader import PlayerLoader

import traceback

class GuiLoadLevel(GuiScreen):

    def __init__(self, screen):
        self.__parent = screen
        self.__finished = False
        self.__loaded = False
        self.__levels = []
        self.__status = ''
        self._title = 'Load level'
        self.__frozen = False
        self.__selectedFile = ''

    def updateScreen(self):
        if self.__selectedFile:
            if self.__selectedFile[-8:] != '.mclevel':
                self.__selectedFile += '.mclevel'

            self._openFile(self.__selectedFile)
            self.__selectedFile = ''
            self.mc.displayGuiScreen(None)

    def _setLevels(self, levels):
        for i in range(5):
            self._controlList[i].enabled = levels[i] != '-'
            self._controlList[i].displayString = levels[i]
            self._controlList[i].visible = True

        self._controlList[5].visible = True

    def initGui(self):
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
        if self.__frozen or not button.enabled:
            return

        if self.__loaded and button.id < 5:
            self._openLevel(button.id)
        elif self.__finished or self.__loaded and button.id == 5:
            self.__frozen = True
            GuiLevelDialog(self).run()
        elif self.__finished or self.__loaded and button.id == 6:
            self.mc.displayGuiScreen(self.__parent)

    def _openLevel(self, id_):
        self.mc.displayGuiScreen(None)
        self.mc.grabMouse()

    def drawScreen(self, xm, ym):
        self._drawGradientRect(0, 0, self.width, self.height, 1610941696, -1607454624)
        self.drawCenteredString(self._fontRenderer, self._title, self.width // 2, 20, 0xFFFFFF)
        if not self.__loaded:
            self.drawCenteredString(self._fontRenderer, self.__status, self.width // 2, self.height // 2 - 4, 0xFFFFFF)

        super().drawScreen(xm, ym)

    def _openFile(self, file):
        try:
            world = PlayerLoader(self.mc, self.mc.loadingScreen).load(file)
            self.mc.setLevel(world)
        except Exception as e:
            print(traceback.format_exc())

    def setFile(self, file):
        self.__selectedFile = file

    def setFrozen(self, frozen):
        self.__frozen = False
