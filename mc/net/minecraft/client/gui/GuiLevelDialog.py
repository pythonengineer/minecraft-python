try:
    import wx
except:
    import tkinter as tk
    from tkinter.filedialog import askopenfilename, asksaveasfilename

import os

class GuiLevelDialog:

    def __init__(self, loadLevel):
        self.__screen = loadLevel

    def run(self):
        from mc.net.minecraft.client.gui.GuiSaveLevel import GuiSaveLevel
        saves = os.path.join(self.__screen.mc.mcDataDir, 'saves')
        if not os.path.exists(saves):
            os.mkdir(saves)

        isLoad = not isinstance(self.__screen, GuiSaveLevel)
        try:
            title = 'Load level' if isLoad else 'Save level'
            style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST if isLoad else wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
            app = wx.App(False)
            with wx.FileDialog(None, title, saves, wildcard='MCLEVEL files (*.mclevel)|*.mclevel',
                               style=style) as fileDialog:
                fileDialog.CenterOnParent()
                fileDialog.SetWindowStyleFlag(wx.STAY_ON_TOP)
                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return

                self.__screen.setFile(fileDialog.GetPath())
            wx.GetApp().ExitMainLoop()
        except NameError:
            root = tk.Tk()
            root.wm_attributes('-topmost', True)
            root.withdraw()
            try:
                fileChooser = askopenfilename if isLoad else asksaveasfilename
                file = fileChooser(initialdir=saves,
                                   filetypes=[('Minecraft levels', '*.mclevel')])
                if file:
                    self.__screen.setFile(file)
            finally:
                root.quit()
                root.destroy()
        finally:
            self.__screen.setFrozen(False)
