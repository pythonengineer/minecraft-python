from mc.net.minecraft.gui.LoadLevelScreen import LoadLevelScreen
from mc.net.minecraft.gui.NameLevelScreen import NameLevelScreen

class SaveLevelScreen(LoadLevelScreen):

    def __init__(self, screen):
        super().__init__(screen)
        self._title = 'Save level'

    def _setLevels(self, string):
        for i in range(5):
            self._buttons[i].msg = string[i]
            self._buttons[i].visible = True

    def _loadLevel(self, i):
        self._minecraft.setScreen(NameLevelScreen(self, self._buttons[i].msg, i))
