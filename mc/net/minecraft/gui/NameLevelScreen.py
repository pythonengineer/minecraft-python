from mc.net.minecraft.gui.Screen import Screen
from mc.net.minecraft.gui.Button import Button
from pyglet import window

import gzip

class NameLevelScreen(Screen):

    def __init__(self, screen, name, id_):
        self.__parent = screen
        self.__name = name
        self.__id = id_
        if self.__name == '-':
            self.__name = ''
        self.__title = 'Enter level name:'
        self.__counter = 0

    def init(self, minecraft, width, height):
        super().init(minecraft, width, height)
        self._buttons.clear()
        self._buttons.append(Button(0, self._width // 2 - 100, self._height // 4 + 120, 200, 20, 'Save'))
        self._buttons.append(Button(1, self._width // 2 - 100, self._height // 4 + 144, 200, 20, 'Cancel'))
        self._buttons[0].enabled = len(self.__name.strip()) > 1

    def tick(self):
        self.__counter += 1

    def _buttonClicked(self, button):
        if button.enabled:
            if button.id == 0 and len(self.__name.strip()) > 1:
                #self._minecraft.levelIo.save(self._minecraft.level, self._minecraft.minecraftUri, self._minecraft.user.name, self._minecraft.user.sessionId, self.__name.strip(), self.__id)
                self._minecraft.setScreen(None)
                self._minecraft.grabMouse()
            elif button.id == 1:
                self._minecraft.setScreen(self.__parent)

    def _keyPressed(self, key, char, motion):
        if motion == window.key.MOTION_BACKSPACE and len(self.__name) > 0:
            self.__name = self.__name[:-1]
        elif char:
            if char in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ,.:-_\'*!"#%/()=+?[]{}<>' and len(self.__name) < 64:
                self.__name += char

            self._buttons[0].enabled = len(self.__name.strip()) > 1

    def render(self, xm, ym):
        self._fillGradient(0, 0, self._width, self._height, 1610941696, -1607454624)
        self.drawCenteredString(self.__title, self._width / 2, 40, 0xFFFFFF)
        i3 = self._width // 2 - 100
        i4 = self._height // 2 - 10
        self._fill(i3 - 1, i4 - 1, i3 + 200 + 1, i4 + 20 + 1, -6250336)
        self._fill(i3, i4, i3 + 200, i4 + 20, 0xFF000000)
        self.drawString(self.__name + ('_' if self.__counter // 6 % 2 == 0 else ''), i3 + 4, i4 + 6, 14737632)
        super().render(xm, ym)
