from mc.net.minecraft.gui.Screen import Screen
from mc.net.minecraft.gui.Button import Button

try:
    import wx
except:
    import tkinter as tk
    from tkinter.filedialog import askopenfilename, asksaveasfilename

import gzip

class LoadLevelScreen(Screen):

    def __init__(self, screen):
        self._parent = screen
        self.__finished = False
        self.__loaded = False
        self.__levels = []
        self.__status = ''
        self._title = 'Load level'
        self.fileLoaded = False
        self._isSaveScreen = False
        self._levelFile = ''

    def run(self):
        try:
            title = 'Save mine file' if self._isSaveScreen else 'Open mine file'
            style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT if self._isSaveScreen else wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
            app = wx.App(False)
            with wx.FileDialog(None, title, wildcard='MINE files (*.mine)|*.mine',
                               style=style) as fileDialog:
                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return

                self._levelFile = fileDialog.GetPath()
            wx.GetApp().ExitMainLoop()
            print(self._levelFile)
        except NameError:
            root = tk.Tk()
            root.withdraw()
            try:
                fileChooser = asksaveasfilename if self._isSaveScreen else askopenfilename
                self._levelFile = fileChooser(filetypes=[('Minecraft levels', '*.mine')])
            finally:
                root.quit()

        self.fileLoaded = False

    def _setLevels(self, levels):
        for i in range(5):
            self._buttons[i].enabled = levels[i] != '-'
            self._buttons[i].msg = levels[i]
            self._buttons[i].visible = True

    def init(self, minecraft, width, height):
        super().init(minecraft, width, height)

        for i in range(5):
            self._buttons.append(Button(i, self._width // 2 - 100, self._height // 6 + i * 24, '---'))
            self._buttons[i].visible = False
            self._buttons[i].enabled = False

        self._buttons.append(Button(5, self._width // 2 - 100, self._height // 6 + 120 + 12, 'Load file...'))
        self._buttons.append(Button(6, self._width // 2 - 100, self._height // 6 + 168, 'Cancel'))

        self.__status = 'Failed to load levels'
        self.__finished = True

    def _buttonClicked(self, button):
        if self.fileLoaded or not button.enabled:
            return

        if self.__loaded and button.id < 5:
            self._loadLevel(button.id)
        elif self.__finished or self.__loaded and button.id == 5:
            self.fileLoaded = True
            self.run()
        elif self.__finished or self.__loaded and button.id == 6:
            self._minecraft.setScreen(self._parent)

    def _loadFile(self, fileName):
        level = self._minecraft.levelIo.load(gzip.open(fileName, 'rb'))
        if level:
            self._minecraft.loadLevel(level)

        self._minecraft.setScreen(self._parent)

    def _loadLevel(self, id_):
        self._minecraft.loadLevel(self._minecraft.user.name, id_)
        self._minecraft.setScreen(None)
        self._minecraft.grabMouse()

    def render(self, xm, ym):
        self._fillGradient(0, 0, self._width, self._height, 1610941696, -1607454624)
        self.drawCenteredString(self._font, self._title, self._width // 2, 20, 0xFFFFFF)
        if self.fileLoaded:
            self.drawCenteredString(self._font, 'Selecting file..', self._width // 2, self._height // 2 - 4, 0xFFFFFF)
        elif not self.__loaded:
            self.drawCenteredString(self._font, self.__status, self._width // 2, self._height // 2 - 4, 0xFFFFFF)
            super().render(xm, ym)

    def tick(self):
        super().tick()
        if self._levelFile:
            self._loadFile(self._levelFile)
            self._levelFile = ''
