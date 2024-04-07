from mc.net.minecraft.client.gui.GuiButton import GuiButton

class GuiButtonSmall(GuiButton):

    def __init__(self, id_, x, y, msg):
        super().__init__(id_, x, y, 150, 20, msg)
