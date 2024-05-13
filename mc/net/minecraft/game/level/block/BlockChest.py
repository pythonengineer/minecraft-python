from mc.net.minecraft.game.level.block.tileentity.TileEntityChest import TileEntityChest
from mc.net.minecraft.game.level.block.BlockContainer import BlockContainer
from mc.net.minecraft.game.InventoryLargeChest import InventoryLargeChest
from mc.net.minecraft.game.item.ItemStack import ItemStack
from mc.JavaUtils import Random

class BlockChest(BlockContainer):

    def __init__(self, blocks, blockId):
        super().__init__(blocks, 54)
        self.blockIndexInTexture = 26
        self.__random = Random()

    def getBlockTextureFromSideAndMetadata(self, world, x, y, z, layer):
        if layer == 1:
            return self.blockIndexInTexture - 1
        elif layer == 0:
            return self.blockIndexInTexture - 1

        north = world.getBlockId(x, y, z - 1)
        south = world.getBlockId(x, y, z + 1)
        west = world.getBlockId(x - 1, y, z)
        east = world.getBlockId(x + 1, y, z)
        if north != self.blockID and south != self.blockID:
            if west != self.blockID and east != self.blockID:
                face = 3
                if self.blocks.opaqueCubeLookup[north] and not \
                   self.blocks.opaqueCubeLookup[south]:
                    face = 3
                if self.blocks.opaqueCubeLookup[south] and not \
                   self.blocks.opaqueCubeLookup[north]:
                    face = 2
                if self.blocks.opaqueCubeLookup[west] and not \
                   self.blocks.opaqueCubeLookup[east]:
                    face = 5
                if self.blocks.opaqueCubeLookup[east] and not \
                   self.blocks.opaqueCubeLookup[west]:
                    face = 4

                if layer == face:
                    return self.blockIndexInTexture + 1
                else:
                    return self.blockIndexInTexture
            elif layer != 4 and layer != 5:
                texOffset = 0
                if west == self.blockID:
                    texOffset = -1

                adjacent1 = world.getBlockId(
                    x - 1 if west == self.blockID else x + 1, y, z - 1
                )
                adjacent2 = world.getBlockId(
                    x - 1 if west == self.blockID else x + 1, y, z + 1
                )
                if layer == 3:
                    texOffset = -1 - texOffset

                face = 3
                if (self.blocks.opaqueCubeLookup[north] or \
                    self.blocks.opaqueCubeLookup[adjacent1]) and not \
                   self.blocks.opaqueCubeLookup[south] and not \
                   self.blocks.opaqueCubeLookup[adjacent2]:
                    face = 3
                if (self.blocks.opaqueCubeLookup[south] or \
                    self.blocks.opaqueCubeLookup[adjacent2]) and not \
                   self.blocks.opaqueCubeLookup[north] and not \
                   self.blocks.opaqueCubeLookup[adjacent1]:
                    face = 2

                if layer == face:
                    return (self.blockIndexInTexture + 16) + texOffset
                else:
                    return (self.blockIndexInTexture + 32) + texOffset
            else:
                return self.blockIndexInTexture
        elif layer != 2 and layer != 3:
            texOffset = 0
            if north == self.blockID:
                texOffset = -1

            adjacent1 = world.getBlockId(
                x - 1, y, z - 1 if north == self.blockID else z + 1
            )
            adjacent2 = world.getBlockId(
                x + 1, y, z - 1 if north == self.blockID else z + 1
            )
            if layer == 4:
                texOffset = -1 - texOffset

            face = 5
            if (self.blocks.opaqueCubeLookup[west] or \
                self.blocks.opaqueCubeLookup[adjacent1]) and not \
               self.blocks.opaqueCubeLookup[east] and not \
               self.blocks.opaqueCubeLookup[adjacent2]:
                face = 5
            if (self.blocks.opaqueCubeLookup[east] or \
                self.blocks.opaqueCubeLookup[adjacent2]) and not \
               self.blocks.opaqueCubeLookup[west] and not \
               self.blocks.opaqueCubeLookup[adjacent1]:
                face = 4

            if layer == face:
                return (self.blockIndexInTexture + 16) + texOffset
            else:
                return (self.blockIndexInTexture + 32) + texOffset
        else:
            return self.blockIndexInTexture

    def getBlockTexture(self, face):
        if face == 1:
            return self.blockIndexInTexture - 1
        elif face == 0:
            return self.blockIndexInTexture - 1
        elif face == 3:
            return self.blockIndexInTexture + 1
        else:
            return self.blockIndexInTexture

    def canPlaceBlockAt(self, world, x, y, z):
        chests = 0
        if world.getBlockId(x - 1, y, z) == self.blockID:
            chests += 1
        if world.getBlockId(x + 1, y, z) == self.blockID:
            chests += 1
        if world.getBlockId(x, y, z - 1) == self.blockID:
            chests += 1
        if world.getBlockId(x, y, z + 1) == self.blockID:
            chests += 1

        if chests > 1:
            return False
        elif self.__chestsAround(world, x - 1, y, z):
            return False
        elif self.__chestsAround(world, x + 1, y, z):
            return False
        elif self.__chestsAround(world, x, y, z - 1):
            return False
        else:
            return not self.__chestsAround(world, x, y, z + 1)

    def __chestsAround(self, world, x, y, z):
        if world.getBlockId(x, y, z) != self.blockID:
            return False
        elif world.getBlockId(x - 1, y, z) == self.blockID:
            return True
        elif world.getBlockId(x + 1, y, z) == self.blockID:
            return True
        elif world.getBlockId(x, y, z - 1) == self.blockID:
            return True
        else:
            return world.getBlockId(x, y, z + 1) == self.blockID

    def onBlockRemoval(self, world, x, y, z):
        from mc.net.minecraft.game.entity.misc.EntityItem import EntityItem
        entity = world.getBlockTileEntity(x, y, z)
        for i in range(entity.getSizeInventory()):
            stack = entity.getStackInSlot(i)
            if stack:
                itemX = self.__random.nextFloat() * 0.8 + 0.1
                itemY = self.__random.nextFloat() * 0.8 + 0.1
                itemZ = self.__random.nextFloat() * 0.8 + 0.1
                while stack.stackSize > 0:
                    stackSize = self.__random.nextInt(21) + 10
                    stackSize = min(stackSize, stack.stackSize)
                    stack.stackSize -= stackSize

                    item = EntityItem(world, x + itemX, y + itemY, z + itemZ,
                                      ItemStack(stack.itemID, stackSize))
                    item.motionX = self.__random.nextGaussian() * 0.05
                    item.motionY = self.__random.nextGaussian() * 0.05 + 0.2
                    item.motionZ = self.__random.nextGaussian() * 0.05
                    world.spawnEntityInWorld(item)

        super().onBlockRemoval(world, x, y, z)

    def blockActivated(self, world, x, y, z, player):
        entity = world.getBlockTileEntity(x, y, z)
        if world.isBlockNormalCube(x, y + 1, z):
            return True
        elif world.getBlockId(x - 1, y, z) == self.blockID and \
             world.isBlockNormalCube(x - 1, y + 1, z):
            return True
        elif world.getBlockId(x + 1, y, z) == self.blockID and \
             world.isBlockNormalCube(x + 1, y + 1, z):
            return True
        elif world.getBlockId(x, y, z - 1) == self.blockID and \
             world.isBlockNormalCube(x, y + 1, z - 1):
            return True
        elif world.getBlockId(x, y, z + 1) == self.blockID and \
             world.isBlockNormalCube(x, y + 1, z + 1):
            return True
        else:
            if world.getBlockId(x - 1, y, z) == self.blockID:
                entity = InventoryLargeChest(
                    'Large chest', world.getBlockTileEntity(x - 1, y, z), entity
                )
            if world.getBlockId(x + 1, y, z) == self.blockID:
                entity = InventoryLargeChest(
                    'Large chest', entity, world.getBlockTileEntity(x + 1, y, z)
                )
            if world.getBlockId(x, y, z - 1) == self.blockID:
                entity = InventoryLargeChest(
                    'Large chest', world.getBlockTileEntity(x, y, z - 1), entity
                )
            if world.getBlockId(x, y, z + 1) == self.blockID:
                entity = InventoryLargeChest(
                    'Large chest', entity, world.getBlockTileEntity(x, y, z + 1)
                )

            player.displayGUIChest(entity)
            return True

    def _getBlockEntity(self):
        return TileEntityChest()
