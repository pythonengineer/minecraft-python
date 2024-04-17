from mc.net.minecraft.game.level.block.Blocks import blocks
from mc.net.minecraft.game.item.Item import Item

class ItemBlock(Item):

    def __init__(self, itemId):
        super().__init__(itemId)
        self.__blockID = itemId

    def onItemUse(self, stack, world, x, y, z, sideHit):
        if sideHit == 0: y -= 1
        if sideHit == 1: y += 1
        if sideHit == 2: z -= 1
        if sideHit == 3: z += 1
        if sideHit == 4: x -= 1
        if sideHit == 5: x += 1

        if not stack.stackSize:
            return

        if x <= 0 or y <= 0 or z <= 0 or x >= world.width - 1 or y >= world.height - 1 or z >= world.length - 1:
            return

        block = blocks.blocksList[world.getBlockId(x, y, z)]
        if self.__blockID <= 0 or block and block != blocks.waterMoving and \
           block != blocks.waterStill and block != blocks.lavaMoving and \
           block != blocks.lavaStill and block != blocks.fire:
            return

        block = blocks.blocksList[self.__blockID]
        aabb = block.getCollisionBoundingBoxFromPool(x, y, z)
        if not world.checkIfAABBIsClear(aabb):
            return

        world.setBlockWithNotify(x, y, z, self.__blockID)
        x += 0.5
        y += 0.5
        z += 0.5
        name = 'step.' + block.stepSound.soundDir
        volume = (block.stepSound.soundVolume + 1.0) / 2.0
        world.playSoundEffect(x, y, z, name, volume, block.stepSound.soundPitch * 0.8)
        stack.stackSize -= 1
