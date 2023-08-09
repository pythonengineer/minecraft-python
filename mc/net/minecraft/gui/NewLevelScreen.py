from mc.net.minecraft.gui.Screen import Screen
from mc.net.minecraft.gui.Button import Button
from pyglet import window

class NewLevelScreen(Screen):

    def __init__(self, screen):
        self.__parent = screen

    def init(self, minecraft, width, height):
        super().init(minecraft, width, height)
        self._buttons.clear()
        self._buttons.append(Button(0, self._width // 2 - 100, self._height // 3, 200, 20, 'Small'))
        self._buttons.append(Button(1, self._width // 2 - 100, self._height // 3 + 32, 200, 20, 'Normal'))
        self._buttons.append(Button(2, self._width // 2 - 100, self._height // 3 + 64, 200, 20, 'Huge'))
        self._buttons.append(Button(3, self._width // 2 - 100, self._height // 3 + 96, 200, 20, 'Cancel'))

    def _buttonClicked(self, button):
        if button.id == 3:
            self._minecraft.setScreen(self.__parent)
        else:
            self._minecraft.generateLevel(button.id)
            self._minecraft.setScreen(None)
            self._minecraft.grabMouse()

    def render(self, xm, ym):
        self._fillGradient(0, 0, self._width, self._height, 1610941696, -1607454624)
        self.drawCenteredString('Generate new level', self._width // 2, 40, 0xFFFFFF)
        super().render(xm, ym)
