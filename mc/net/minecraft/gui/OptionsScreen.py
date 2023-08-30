from mc.net.minecraft.gui.Screen import Screen
from mc.net.minecraft.gui.Button import Button
from mc.net.minecraft.gui.ControlsScreen import ControlsScreen

class OptionsScreen(Screen):
    __title = 'Options'

    def __init__(self, screen, options):
        self.__parent = screen
        self.__options = options

    def init(self, minecraft, width, height):
        super().init(minecraft, width, height)
        for i in range(5):
            self._buttons.append(Button(i, self._width // 2 - 100, self._height // 6 + i * 24, self.__options.getOption(i)))

        self._buttons.append(Button(10, self._width // 2 - 100, self._height // 6 + 120 + 12, 'Controls...'))
        self._buttons.append(Button(20, self._width // 2 - 100, self._height // 6 + 168, 'Done'))

    def _buttonClicked(self, button):
        if button.enabled:
            if button.id < 5:
                self.__options.setOption(button.id, 1)
                button.msg = self.__options.getOption(button.id)
            elif button.id == 10:
                self._minecraft.setScreen(ControlsScreen(self, self.__options))
            elif button.id == 20:
                self._minecraft.setScreen(self.__parent)

    def render(self, xm, ym):
        self._fillGradient(0, 0, self._width, self._height, 1610941696, -1607454624)
        self.drawCenteredString(self._font, self.__title, self._width / 2, 20, 16777215)
        super().render(xm, ym)
