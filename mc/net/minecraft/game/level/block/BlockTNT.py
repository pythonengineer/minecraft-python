from mc.net.minecraft.game.level.block.Block import Block
from mc.net.minecraft.game.level.material.Material import Material
from mc.net.minecraft.game.entity.misc.EntityTNTPrimed import EntityTNTPrimed

class BlockTNT(Block):

    def __init__(self, blocks, blockId, tex):
        super().__init__(blocks, 46, 8, Material.tnt)

    def getBlockTexture(self, face):
        if face == 0:
            return self.blockIndexInTexture + 2
        elif face == 1:
            return self.blockIndexInTexture + 1
        else:
            return self.blockIndexInTexture

    def quantityDropped(self, random):
        return 0

    def onBlockDestroyedByExplosion(self, world, x, y, z):
        entity = EntityTNTPrimed(world, x + 0.5, y + 0.5, z + 0.5)
        entity.fuse = world.rand.nextInt(entity.fuse // 4) + entity.fuse // 8
        world.spawnEntityInWorld(entity)

    def onBlockDestroyedByPlayer(self, world, x, y, z):
        entity = EntityTNTPrimed(world, x + 0.5, y + 0.5, z + 0.5)
        world.spawnEntityInWorld(entity)
        world.playSoundAtEntity(entity, 'random.fuse', 1.0, 1.0)
