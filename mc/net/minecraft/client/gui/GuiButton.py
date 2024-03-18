from mc.net.minecraft.client.gui.Gui import Gui

class GuiButton(Gui):

    def __init__(self, id_, x, y, width, height=None, string=None):
        if height is None:
            string = width
            width = 200
            height = 20

        self.id = id_
        self.width = width
        self.height = 20
        self.x = x
        self.y = y
        self.displayString = string
        self.enabled = True
        self.visible = True
