from mc.net.minecraft.gui.Screen import Screen
from mc.net.minecraft.gui.Button import Button
from pyglet import window

class PauseScreen(Screen):
    buttons = set()

    def init(self, minecraft, width, height):
        super().init(minecraft, width, height)
        self.buttons.add(Button(0, self.width // 2 - 100, self.height // 3 + 0, 200, 20, 'Generate new level'))
        self.buttons.add(Button(1, self.width // 2 - 100, self.height // 3 + 32, 200, 20, 'Save level..'))
        self.buttons.add(Button(2, self.width // 2 - 100, self.height // 3 + 64, 200, 20, 'Load level..'))
        self.buttons.add(Button(3, self.width // 2 - 100, self.height // 3 + 96, 200, 20, 'Back to game'))

    def _keyPressed(self, key):
        pass

    def _mouseClicked(self, x, y, buttonNum):
        if buttonNum == window.mouse.LEFT:
            for button in self.buttons:
                if x >= button.x and y >= button.y and x < button.x + button.w and y < button.y + button.h:
                    self.__buttonClicked(button)

    def __buttonClicked(self, button):
        if button.id == 0:
            self.minecraft.generateNewLevel()
            self.minecraft.setScreen(None)
            self.minecraft.grabMouse()
        elif button.id == 1:
            self.minecraft._attemptSaveLevel()
        elif button.id == 3:
            self.minecraft.setScreen(None)
            self.minecraft.grabMouse()

    def render(self, xm, ym):
        self._fillGradient(0, 0, self.width, self.height, 537199872, -1607454624)

        for button in self.buttons:
            self._fill(button.x - 1, button.y - 1, button.x + button.w + 1, button.y + button.h + 1, -16777216)
            if xm >= button.x and ym >= button.y and xm < button.x + button.w and ym < button.y + button.h:
                self._fill(button.x - 1, button.y - 1, button.x + button.w + 1, button.y + button.h + 1, -6250336)
                self._fill(button.x, button.y, button.x + button.w, button.y + button.h, -8355680)
                self.drawCenteredString(button.msg, button.x + button.w // 2, button.y + (button.h - 8) // 2, 16777120)
            else:
                self._fill(button.x, button.y, button.x + button.w, button.y + button.h, -9408400)
                self.drawCenteredString(button.msg, button.x + button.w // 2, button.y + (button.h - 8) // 2, 14737632)
