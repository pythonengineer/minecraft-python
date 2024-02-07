from mc.net.minecraft.gui.LoadLevelScreen import LoadLevelScreen
from mc.net.minecraft.gui.NameLevelScreen import NameLevelScreen

import gzip

class SaveLevelScreen(LoadLevelScreen):

    def __init__(self, screen):
        super().__init__(screen)
        self._title = 'Save level'
        self._isSaveScreen = True

    def init(self, minecraft, width, height):
        super().init(minecraft, width, height)
        self._buttons[5].msg = 'Save file...'

    def _setLevels(self, levels):
        for i in range(5):
            self._buttons[i].msg = levels[i]
            self._buttons[i].visible = True
            self._buttons[i].enabled = True

    def _loadFile(self, fileName):
        if fileName[-5:] != '.mine':
            fileName += '.mine'

        self._minecraft.levelIo.save(self._minecraft.level, gzip.open(fileName, 'wb'))
        self._minecraft.setScreen(self._parent)

    def _loadLevel(self, i):
        self._minecraft.setScreen(NameLevelScreen(self, self._buttons[i].msg, i))
