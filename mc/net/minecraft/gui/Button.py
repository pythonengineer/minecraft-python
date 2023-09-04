from mc.net.minecraft.gui.GuiComponent import GuiComponent

class Button(GuiComponent):

    def __init__(self, id_, x, y, w, h=None, msg=None):
        if h is None:
            msg = w
            w = 200
            h = 20

        self.id = id_
        self.w = w
        self.h = 20
        self.x = x
        self.y = y
        self.msg = msg
        self.enabled = True
        self.visible = True
