from mc.net.minecraft.gui.Screen import Screen
from mc.net.minecraft.gui.NewLevelScreen import NewLevelScreen
from mc.net.minecraft.gui.SaveLevelScreen import SaveLevelScreen
from mc.net.minecraft.gui.LoadLevelScreen import LoadLevelScreen
from mc.net.minecraft.gui.Button import Button
from pyglet import window

class PauseScreen(Screen):

    def init(self, minecraft, width, height):
        super().init(minecraft, width, height)
        self._buttons.clear()
        self._buttons.append(Button(0, self._width // 2 - 100, self._height // 3, 200, 20, 'Generate new level...'))
        self._buttons.append(Button(1, self._width // 2 - 100, self._height // 3 + 32, 200, 20, 'Save level..'))
        self._buttons.append(Button(2, self._width // 2 - 100, self._height // 3 + 64, 200, 20, 'Load level..'))
        self._buttons.append(Button(3, self._width // 2 - 100, self._height // 3 + 96, 200, 20, 'Back to game'))
        if not False:#self._minecraft.user:
            self._buttons[2].enabled = False

        if minecraft.connectionManager:
            self._buttons[0].enabled = False
            self._buttons[1].enabled = False
            self._buttons[2].enabled = False

    def _buttonClicked(self, button):
        if button.id == 0:
            self._minecraft.setScreen(NewLevelScreen(self))

        if False:
            if button.id == 1 and self._minecraft.user:
                self._minecraft.setScreen(SaveLevelScreen(self))
            elif button.id == 2 and self._minecraft.user:
                self._minecraft.setScreen(LoadLevelScreen(self))
        elif button.id == 1:
            self._minecraft.saveLevel(None, None)

        if button.id == 3:
            self._minecraft.setScreen(None)
            self._minecraft.grabMouse()

    def render(self, xm, ym):
        self._fillGradient(0, 0, self._width, self._height, 1610941696, -1607454624)
        self.drawCenteredString('Game menu', self._width // 2, 40, 0xFFFFFF)
        super().render(xm, ym)
