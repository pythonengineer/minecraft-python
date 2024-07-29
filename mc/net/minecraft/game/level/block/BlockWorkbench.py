from mc.net.minecraft.game.level.block.Block import Block

class BlockWorkbench(Block):

    def __init__(self, blocks, blockId):
        super().__init__(blocks, 58)
        self.blockIndexInTexture = 59

    def getBlockTextureFromSideAndMetadata(self, world, x, y, z, layer):
        if layer == 1:
            return self.blockIndexInTexture - 16
        elif layer == 0:
            return self.blocks.wood.getBlockTexture(0)
        elif layer != 2 and layer != 3:
            return self.blockIndexInTexture
        else:
            return self.blockIndexInTexture + 1

    def getBlockTexture(self, face):
        if face == 1:
            return self.blockIndexInTexture - 16
        elif face == 0:
            return self.blocks.wood.getBlockTexture(0)
        elif face != 2 and face != 4:
            return self.blockIndexInTexture
        else:
            return self.blockIndexInTexture + 1

    def blockActivated(self, world, x, y, z, player):
        player.displayWorkbenchGUI()
        return True
