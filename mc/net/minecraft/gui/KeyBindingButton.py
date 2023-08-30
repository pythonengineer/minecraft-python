from mc.net.minecraft.gui.Button import Button

class KeyBindingButton(Button):

    def __init__(self, id_, w, h, msg):
        super().__init__(id_, w, h, 150, 20, msg)
