from mc.net.minecraft.gui.Screen import Screen
from mc.net.minecraft.gui.Button import Button

class LoadLevelScreen(Screen):

    def __init__(self, screen):
        self.__parent = screen
        self.__finished = False
        self.__loaded = False
        self.__levels = []
        self.__status = ''
        self._title = 'Load level'

    def run(self):
        """
        This is left incomplete as the original code relies on minecraft.net/listmaps.jsp
        which no longer exists.
        """

        self.__status = 'Failed to load levels'
        self.__finished = True

    def _setLevels(self, strings):
        for i in range(5):
            self._buttons[i].enabled = strings[i] != '-'
            self._buttons[i].msg = strings[i]
            self._buttons[i].visible = True

    def init(self, minecraft, width, height):
        super().init(minecraft, width, height)

        for i in range(5):
            self._buttons.append(Button(i, self._width // 2 - 100, self._height // 4 + i * 24, 200, 20, '---'))
            self._buttons[i].visible = False

        self._buttons.append(Button(5, self._width // 2 - 100, self._height // 4 + 144, 200, 20, 'Cancel'))

        self.run()

    def _buttonClicked(self, button):
        if button.enabled:
            if self.__loaded and button.id < 5:
                self._loadLevel(button.id)

            if self.__finished or self.__loaded and button.id == 5:
                self._minecraft.setScreen(self.__parent)

    def _loadLevel(self, id_):
        self._minecraft.loadLevel(self._minecraft.user.name, id_)
        self._minecraft.setScreen(None)
        self._minecraft.grabMouse()

    def render(self, xm, ym):
        self._fillGradient(0, 0, self._width, self._height, 1610941696, -1607454624)
        self.drawCenteredString(self._title, self._width / 2, 40, 0xFFFFFF)
        if not self.__loaded:
            self.drawCenteredString(self.__status, self._width // 2, self._height // 2 - 4, 0xFFFFFF)

        super().render(xm, ym)
