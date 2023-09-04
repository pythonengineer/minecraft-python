from mc.net.minecraft.gui.Button import Button

class SmallButton(Button):

    def __init__(self, id_, x, y, msg):
        super().__init__(id_, x, y, 150, 20, msg)
