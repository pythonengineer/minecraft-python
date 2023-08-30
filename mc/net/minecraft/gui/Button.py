from mc.net.minecraft.gui.Gui import Gui

class Button(Gui):

    def __init__(self, id_, w, h, x, y=None, msg=None):
        if y is None:
            msg = x
            x = 200
            y = 20

        self.id = id_
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.msg = msg
        self.enabled = True
        self.visible = True
