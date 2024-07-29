from mc.net.minecraft.game.level.block.Block import Block
from mc.net.minecraft.game.level.material.Material import Material

class BlockTorch(Block):

    def __init__(self, blocks, blockId, tex):
        super().__init__(blocks, 50, 80, Material.circuits)

    def getCollisionBoundingBoxFromPool(self, x, y, z):
        return None

    def isOpaqueCube(self):
        return False

    def renderAsNormalBlock(self):
        return False

    def getRenderType(self):
        return 2

    def collisionRayTrace(self, world, x, y, z, v0, v1):
        if world.isBlockNormalCube(x - 1, y, z):
            self._setBlockBounds(0.0, 0.2, 0.35, 0.3, 0.8, 0.65)
        elif world.isBlockNormalCube(x + 1, y, z):
            self._setBlockBounds(0.7, 0.2, 0.35, 1.0, 0.8, 0.65)
        elif world.isBlockNormalCube(x, y, z - 1):
            self._setBlockBounds(0.35, 0.2, 0.0, 0.65, 0.8, 0.3)
        elif world.isBlockNormalCube(x, y, z + 1):
            self._setBlockBounds(0.35, 0.2, 0.7, 0.65, 0.8, 1.0)
        else:
            self._setBlockBounds(0.4, 0.0, 0.4, 0.6, 0.6, 0.6)

        return super().collisionRayTrace(world, x, y, z, v0, v1)

    def randomDisplayTick(self, world, x, y, z, random):
        posX = x + 0.5
        posY = y + 0.7
        posZ = z + 0.5
        if world.isBlockNormalCube(x - 1, y, z):
            world.spawnParticle('smoke', posX - 0.27, posY + 0.22, posZ, 0.0, 0.0, 0.0)
            world.spawnParticle('flame', posX - 0.27, posY + 0.22, posZ, 0.0, 0.0, 0.0)
        elif world.isBlockNormalCube(x + 1, y, z):
            world.spawnParticle('smoke', posX + 0.27, posY + 0.22, posZ, 0.0, 0.0, 0.0)
            world.spawnParticle('flame', posX + 0.27, posY + 0.22, posZ, 0.0, 0.0, 0.0)
        elif world.isBlockNormalCube(x, y, z - 1):
            world.spawnParticle('smoke', posX, posY + 0.22, posZ - 0.27, 0.0, 0.0, 0.0)
            world.spawnParticle('flame', posX, posY + 0.22, posZ - 0.27, 0.0, 0.0, 0.0)
        elif world.isBlockNormalCube(x, y, z + 1):
            world.spawnParticle('smoke', posX, posY + 0.22, posZ + 0.27, 0.0, 0.0, 0.0)
            world.spawnParticle('flame', posX, posY + 0.22, posZ + 0.27, 0.0, 0.0, 0.0)
        else:
            world.spawnParticle('smoke', posX, posY, posZ, 0.0, 0.0, 0.0)
            world.spawnParticle('flame', posX, posY, posZ, 0.0, 0.0, 0.0)
