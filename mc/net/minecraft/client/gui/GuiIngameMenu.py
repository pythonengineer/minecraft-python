from mc.net.minecraft.client.gui.GuiScreen import GuiScreen
from mc.net.minecraft.client.gui.GuiOptions import GuiOptions
from mc.net.minecraft.client.gui.GuiNewLevel import GuiNewLevel
from mc.net.minecraft.client.gui.GuiSaveLevel import GuiSaveLevel
from mc.net.minecraft.client.gui.GuiLoadLevel import GuiLoadLevel
from mc.net.minecraft.client.gui.GuiButton import GuiButton
from pyglet import window

class GuiIngameMenu(GuiScreen):

    def initGui(self):
        self._controlList.clear()
        self._controlList.append(GuiButton(0, self.width // 2 - 100,
                                           self.height // 4, 'Options...'))
        self._controlList.append(GuiButton(1, self.width // 2 - 100,
                                           self.height // 4 + 24, 'Generate new world...'))
        self._controlList.append(GuiButton(2, self.width // 2 - 100,
                                           self.height // 4 + 48, 'Save world..'))
        self._controlList.append(GuiButton(3, self.width // 2 - 100,
                                           self.height // 4 + 72, 'Load world..'))
        self._controlList.append(GuiButton(4, self.width // 2 - 100,
                                           self.height // 4 + 120, 'Back to game'))
        if not self.mc.session:
            self._controlList[2].enabled = False
            self._controlList[3].enabled = False

    def _actionPerformed(self, button):
        if button.id == 0:
            self.mc.displayGuiScreen(GuiOptions(self, self.mc.options))
        elif button.id == 1:
            self.mc.displayGuiScreen(GuiNewLevel(self))
        elif button.id == 2 and self.mc.session:
            self.mc.displayGuiScreen(GuiSaveLevel(self))
        elif button.id == 3 and self.mc.session:
            self.mc.displayGuiScreen(GuiLoadLevel(self))
        elif button.id == 4:
            self.mc.displayGuiScreen(None)
            self.mc.grabMouse()

    def drawScreen(self, xm, ym):
        self._drawGradientRect(0, 0, self.width, self.height, 1610941696, -1607454624)
        self.drawCenteredString(self._fontRenderer, 'Game menu', self.width // 2, 40, 0xFFFFFF)
        super().drawScreen(xm, ym)
