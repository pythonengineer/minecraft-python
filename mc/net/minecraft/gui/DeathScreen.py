from mc.net.minecraft.gui.LoadLevelScreen import LoadLevelScreen
from mc.net.minecraft.gui.NewLevelScreen import NewLevelScreen
from mc.net.minecraft.gui.OptionsScreen import OptionsScreen
from mc.net.minecraft.gui.Screen import Screen
from mc.net.minecraft.gui.Button import Button
from pyglet import gl

class DeathScreen(Screen):

    def init(self, minecraft, width, height):
        super().init(minecraft, width, height)
        self._buttons.clear()
        self._buttons.append(Button(1, self._width // 2 - 100, self._height // 4 + 72, 'Generate new level...'))
        self._buttons.append(Button(2, self._width // 2 - 100, self._height // 4 + 96, 'Load level..'))
        if not self._minecraft.user:
            self._buttons[2].enabled = False

    def _buttonClicked(self, button):
        if button.id == 0:
            self._minecraft.setScreen(OptionsScreen(self, self._minecraft.options))
        elif button.id == 1:
            self._minecraft.setScreen(NewLevelScreen(self))
        elif button.id == 2 and self._minecraft.user:
            self._minecraft.setScreen(LoadLevelScreen(self))

    def render(self, xm, ym):
        self._fillGradient(0, 0, self._width, self._height, 0x60500000, -1602211792)
        gl.glPushMatrix()
        gl.glScalef(2.0, 2.0, 2.0)
        self.drawCenteredString(self._font, 'Game over!', self._width // 2 // 2, 30, 0xFFFFFF)
        gl.glPopMatrix()
        self.drawCenteredString(self._font, 'Score: &e' + str(self._minecraft.player.getScore()), self._width // 2, 100, 0xFFFFFF)
        super().render(xm, ym)
