from mc.net.minecraft.client.gui.GuiScreen import GuiScreen
from mc.net.minecraft.client.gui.GuiButton import GuiButton
from pyglet import window

class GuiSaveBase(GuiScreen):

    def __init__(self, screen, name, slot):
        self.__prevScr = screen
        self.__saveSlot = name
        if self.__saveSlot == '-':
            self.__saveSlot = ''
        self.__slot = slot
        self.__title = 'Enter level name:'
        self.__id = 0

    def initGui(self, minecraft, width, height):
        super().initGui(minecraft, width, height)
        self._controlList.clear()
        self._controlList.append(GuiButton(0, self.width // 2 - 100, self.height // 4 + 120, 'Save'))
        self._controlList.append(GuiButton(1, self.width // 2 - 100, self.height // 4 + 144, 'Cancel'))
        self._controlList[0].enabled = len(self.__saveSlot.strip()) > 1

    def updateScreen(self):
        self.__id += 1

    def _actionPerformed(self, button):
        if button.enabled:
            if button.id == 0 and len(self.__saveSlot.strip()) > 1:
                self.__saveSlot.strip()
                self._mc.displayGuiScreen(None)
                self._mc.setIngameFocus()
            elif button.id == 1:
                self._mc.displayGuiScreen(self.__prevScr)

    def _keyTyped(self, key, char, motion):
        if motion == window.key.MOTION_BACKSPACE and len(self.__saveSlot) > 0:
            self.__saveSlot = self.__saveSlot[:-1]
        elif char:
            if char in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ,.:-_\'*!"#%/()=+?[]{}<>' and len(self.__saveSlot) < 64:
                self.__saveSlot += char

            self._controlList[0].enabled = len(self.__saveSlot.strip()) > 1

    def drawScreen(self, xm, ym):
        self._drawGradientRect(0, 0, self.width, self.height, 1610941696, -1607454624)
        self.drawCenteredString(self._font, self.__title, self.width / 2, 40, 0xFFFFFF)
        w = self.width // 2 - 100
        h = self.height // 2 - 10
        self._drawRect(w - 1, h - 1, w + 200 + 1, h + 20 + 1, -6250336)
        self._drawRect(w, h, w + 200, h + 20, -16777216)
        self._font.drawStringWithShadow(
            self.__saveSlot + ('_' if self.__id // 6 % 2 == 0 else ''),
            w + 4, h + 6, 14737632
        )
        super().drawScreen(xm, ym)
