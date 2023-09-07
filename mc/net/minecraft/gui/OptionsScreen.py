from mc.net.minecraft.gui.Screen import Screen
from mc.net.minecraft.gui.Button import Button
from mc.net.minecraft.gui.SmallButton import SmallButton
from mc.net.minecraft.gui.ControlsScreen import ControlsScreen

class OptionsScreen(Screen):
    __title = 'Options'

    def __init__(self, screen, options):
        self.__parent = screen
        self.__options = options

    def init(self, minecraft, width, height):
        super().init(minecraft, width, height)
        for i in range(self.__options.optionCount):
            self._buttons.append(SmallButton(i, self._width // 2 - 155 + i % 2 * 160, self._height // 6 + 24 * (i >> 1), self.__options.getMessage(i)))

        self._buttons.append(Button(100, self._width // 2 - 100, self._height // 6 + 120 + 12, 'Controls...'))
        self._buttons.append(Button(200, self._width // 2 - 100, self._height // 6 + 168, 'Done'))

    def _buttonClicked(self, button):
        if button.enabled:
            if button.id < 100:
                self.__options.setOption(button.id, 1)
                button.msg = self.__options.getMessage(button.id)
            elif button.id == 100:
                self._minecraft.setScreen(ControlsScreen(self, self.__options))
            elif button.id == 200:
                self._minecraft.setScreen(self.__parent)

    def render(self, xm, ym):
        self._fillGradient(0, 0, self._width, self._height, 1610941696, -1607454624)
        self.drawCenteredString(self._font, self.__title, self._width / 2, 20, 16777215)
        super().render(xm, ym)
