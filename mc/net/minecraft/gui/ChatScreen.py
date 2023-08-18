from mc.net.minecraft.gui.Screen import Screen
from mc.net.minecraft.net import Packets
from pyglet import window

class ChatScreen(Screen):
    __typedMsg = ''
    __counter = 0

    def init(self, minecraft, width, height):
        super().init(minecraft, width, height)

    def tick(self):
        self.__counter += 1

    def _keyPressed(self, key, char, motion):
        if char == 'SPACE':
            char = ' '
        if key == window.key.ESCAPE:
            self._minecraft.setScreen(None)
        elif key == window.key.ENTER:
            string = self.__typedMsg.strip().strip()
            if len(string) > 0:
                self._minecraft.connectionManager.connection.sendPacket(Packets.CHAT_MESSAGE, [-1, string])

            self._minecraft.setScreen(None)
        else:
            if motion == window.key.MOTION_BACKSPACE and len(self.__typedMsg) > 0:
                self.__typedMsg = self.__typedMsg[:-1]
            if char and char in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ,.:-_\'*!\\"#%/()=+?[]{}<>@|$;' and len(self.__typedMsg) < 64 - (len(self._minecraft.user.name) + 2):
                self.__typedMsg += char

    def render(self, xm, ym):
        self._fill(2, self._height - 14, self._width - 2, self._height - 2, -2 ** 31)
        self.drawString('> ' + self.__typedMsg + ('_' if self.__counter // 6 % 2 == 0 else ''), 4, self._height - 12, 14737632)
