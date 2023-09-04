from mc.net.minecraft.gui.SmallButton import SmallButton
from mc.net.minecraft.gui.Screen import Screen
from mc.net.minecraft.gui.Button import Button

class ControlsScreen(Screen):
    __title = 'Controls'
    __selectedKey = -1

    def __init__(self, screen, options):
        self.__parent = screen
        self.__options = options

    def init(self, minecraft, width, height):
        super().init(minecraft, width, height)
        for i, binding in enumerate(self.__options.keys):
            self._buttons.append(SmallButton(i, self._width // 2 - 155 + i % 2 * 160, self._height // 6 + 24 * (i >> 1), self.__options.getKeyMessage(i)))

        self._buttons.append(Button(200, self._width // 2 - 100, self._height // 6 + 168, 'Done'))

    def _buttonClicked(self, button):
        for i, binding in enumerate(self.__options.keys):
            self._buttons[i].msg = self.__options.getKeyMessage(i)

        if button.id == 200:
            self._minecraft.setScreen(self.__parent)
        else:
            self.__selectedKey = button.id
            button.msg = '> ' + self.__options.getKeyMessage(button.id) + ' <'

    def _keyPressed(self, key, char, motion):
        if self.__selectedKey >= 0 and key:
            self.__options.setKey(self.__selectedKey, key)
            self._buttons[self.__selectedKey].msg = self.__options.getKeyMessage(self.__selectedKey)
            self.__selectedKey = -1
        else:
            super()._keyPressed(key, char, motion)

    def render(self, xm, ym):
        self._fillGradient(0, 0, self._width, self._height, 1610941696, -1607454624)
        self.drawCenteredString(self._font, self.__title, self._width // 2, 20, 16777215)
        super().render(xm, ym)
