try:
    import wx
except:
    import tkinter as tk
    from tkinter.filedialog import askopenfilename, asksaveasfilename

class GuiLevelDialog:

    def __init__(self, loadLevel):
        self.__guiLoadLevel = loadLevel

    def run(self):
        from mc.net.minecraft.client.gui.GuiSaveLevel import GuiSaveLevel
        isLoad = not isinstance(self.__guiLoadLevel, GuiSaveLevel)
        try:
            title = 'Open mclevel file' if isLoad else 'Save mclevel file'
            style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST if isLoad else wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
            app = wx.App(False)
            with wx.FileDialog(None, title, wildcard='MCLEVEL files (*.mclevel)|*.mclevel',
                               style=style) as fileDialog:
                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return

                self.__guiLoadLevel.setFile(fileDialog.GetPath())
            wx.GetApp().ExitMainLoop()
        except NameError:
            root = tk.Tk()
            root.withdraw()
            try:
                fileChooser = askopenfilename if isLoad else asksaveasfilename
                file = fileChooser(filetypes=[('Minecraft levels', '*.mclevel')])
                if file:
                    self.__guiLoadLevel.setFile(file)
            finally:
                root.quit()
        finally:
            self.__guiLoadLevel.setFrozen(False)
