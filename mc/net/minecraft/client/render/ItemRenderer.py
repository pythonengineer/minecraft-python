from mc.net.minecraft.client.render.RenderBlocks import RenderBlocks
from mc.net.minecraft.client.render.Tessellator import tessellator

class ItemRenderer:

    def __init__(self, minecraft):
        self.minecraft = minecraft
        self.itemToRender = None
        self.equippedProgress = 0.0
        self.prevEquippedProgress = 0.0
        self.swingProgress = 0
        self.itemSwingState = False
        self.renderBlocksInstance = RenderBlocks(tessellator)
