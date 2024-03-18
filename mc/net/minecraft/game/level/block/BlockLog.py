from mc.net.minecraft.game.level.block.Block import Block

import random
import math

class BlockLog(Block):

    def __init__(self, blocks):
        super().__init__(blocks, 17)
        self.blockIndexInTexture = 20

    def quantityDropped(self):
        return math.floor(3 * random.random()) + 3

    def getBlockTexture(self, face):
        return 21 if face == 1 else (21 if face == 0 else 20)
