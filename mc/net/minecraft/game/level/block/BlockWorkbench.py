from mc.net.minecraft.game.level.block.Block import Block
from mc.net.minecraft.game.level.material.Material import Material

class BlockWorkbench(Block):

    def __init__(self, blocks, blockId):
        super().__init__(blocks, 58, Material.wood)
        self.blockIndexInTexture = 59

    def getBlockTexture(self, face):
        if face == 1:
            return self.blockIndexInTexture - 16
        elif face == 0:
            return self.blocks.planks.getBlockTexture(0)
        elif face != 2 and face != 4:
            return self.blockIndexInTexture
        else:
            return self.blockIndexInTexture + 1

    def blockActivated(self, world, x, y, z, player):
        player.displayWorkbenchGUI()
        return True
