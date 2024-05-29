from mc.net.minecraft.client.controller.PlayerController import PlayerController
from mc.net.minecraft.game.level.MobSpawner import MobSpawner
from mc.net.minecraft.game.level.block.Blocks import blocks
from mc.net.minecraft.game.entity.EntityLiving import EntityLiving
from mc.net.minecraft.game.item.ItemStack import ItemStack
from mc.net.minecraft.game.item.Items import items

class PlayerControllerSP(PlayerController):

    def __init__(self, mc):
        super().__init__(mc)
        self.__curBlockX = -1
        self.__curBlockY = -1
        self.__curBlockZ = -1
        self.__curBlockDamage = 0
        self.__prevBlockDamage = 0
        self.__blockHitWait = 0
        self.__mobSpawner = None
        self.__mainChestArray = (
            blocks.stone, blocks.grass, blocks.cobblestone, blocks.planks, blocks.sapling,
            blocks.bedrock, blocks.sand, blocks.gravel, blocks.oreGold, blocks.oreIron,
            blocks.oreCoal, blocks.wood, blocks.leaves, blocks.sponge, blocks.glass,
            blocks.plantYellow, blocks.plantRed, blocks.mushroomBrown, blocks.mushroomRed,
            blocks.blockGold, blocks.blockSteel, blocks.stairSingle, blocks.brick, blocks.tnt,
            blocks.bookShelf, blocks.cobblestoneMossy, blocks.obsidian, blocks.torch,
            blocks.waterSource, blocks.lavaSource, blocks.chest
        )
        self.__woolChestArray = (
            blocks.clothRed, blocks.clothOrange, blocks.clothYellow,
            blocks.clothChartreuse, blocks.clothGreen, blocks.clothSpringGreen,
            blocks.clothCyan, blocks.clothCapri, blocks.clothUltramarine,
            blocks.clothViolet, blocks.clothPurple, blocks.clothMagenta,
            blocks.clothRose, blocks.clothDarkGray, blocks.clothGray, blocks.clothWhite
        )

    def flipPlayer(self, player):
        x = int(player.posX)
        y = int(player.posY)
        z = int(player.posZ)
        for xx in range(x - 3, x + 4):
            for yy in range(y - 2, y + 3):
                for zz in range(z - 3, z + 4):
                    blockId = blocks.obsidian.blockID if yy < y - 1 else 0
                    if xx == x - 3 or zz == z - 3 or xx == x + 3 or zz == z + 3 or yy == y - 2 or yy == y + 2:
                        blockId = blocks.cobblestoneMossy.blockID

                    if yy == y and zz == z and (xx == x - 3 + 1 or xx == x + 3 - 1):
                        blockId = blocks.torch.blockID

                    if zz == z - 3 and xx == x and yy >= y - 1 and yy <= y:
                        blockId = 0

                    self._mc.theWorld.setBlockWithNotify(xx, yy, zz, blockId)

        self._mc.theWorld.setBlockWithNotify(x - 2, y - 1, z - 2, blocks.chest.blockID)
        itemsChest = self._mc.theWorld.getBlockTileEntity(x - 2, y - 1, z - 2)
        self._mc.theWorld.setBlockWithNotify(x + 2, y - 1, z - 2, blocks.chest.blockID)
        blocksChest1 = self._mc.theWorld.getBlockTileEntity(x + 2, y - 1, z - 2)
        self._mc.theWorld.setBlockWithNotify(x + 2, y - 1, z - 1, blocks.chest.blockID)
        blocksChest2 = self._mc.theWorld.getBlockTileEntity(x + 2, y - 1, z - 1)
        self._mc.theWorld.setBlockWithNotify(x - 1, y - 1, z + 2, blocks.chest.blockID)
        tntChest1 = self._mc.theWorld.getBlockTileEntity(x - 1, y - 1, z + 2)
        self._mc.theWorld.setBlockWithNotify(x, y - 1, z + 2, blocks.chest.blockID)
        tntChest2 = self._mc.theWorld.getBlockTileEntity(x, y - 1, z + 2)
        self._mc.theWorld.setBlockWithNotify(x + 2, y - 1, z + 1, blocks.chest.blockID)
        woolChest = self._mc.theWorld.getBlockTileEntity(x + 2, y - 1, z + 1)
        slot = 0
        for i in range(256, 1024):
            if items.itemsList[i]:
                limit = items.itemsList[i].getItemStackLimit()
                itemsChest.setInventorySlotContents(slot, ItemStack(i, limit))
                slot += 1
                if slot >= 27:
                    break

        for slot in range(27):
            blockId = blocks.tnt.blockID
            stack = ItemStack(blockId, items.itemsList[blockId].getItemStackLimit())
            tntChest1.setInventorySlotContents(slot, stack)
            stack = ItemStack(blockId, items.itemsList[blockId].getItemStackLimit())
            tntChest2.setInventorySlotContents(slot, stack)

        for slot in range(min(len(self.__mainChestArray), 54)):
            blockId = self.__mainChestArray[slot]
            stack = ItemStack(blockId, items.itemsList[blockId.blockID].getItemStackLimit())
            if slot >= 27:
                blocksChest2.setInventorySlotContents(slot - 27, stack)
            else:
                blocksChest1.setInventorySlotContents(slot, stack)

        for slot in range(min(len(self.__woolChestArray), 54)):
            stack = ItemStack(
                self.__woolChestArray[slot],
                items.itemsList[self.__woolChestArray[slot].blockID].getItemStackLimit()
            )
            woolChest.setInventorySlotContents(slot, stack)

    def sendBlockRemoved(self, x, y, z):
        block = self._mc.theWorld.getBlockId(x, y, z)
        change = super().sendBlockRemoved(x, y, z)
        if change:
            blocks.blocksList[block].dropBlockAsItem(self._mc.theWorld, x, y, z)

        return change

    def clickBlock(self, x, y, z):
        block = self._mc.theWorld.getBlockId(x, y, z)
        if block > 0 and blocks.blocksList[block].blockStrength(self._mc.thePlayer) <= 0:
            self.sendBlockRemoved(x, y, z)

    def resetBlockRemoving(self):
        self.__curBlockDamage = 0
        self.__blockHitWait = 0

    def sendBlockRemoving(self, x, y, z, sideHit):
        if self.__blockHitWait > 0:
            self.__blockHitWait -= 1
            return

        super().sendBlockRemoving(x, y, z, sideHit)
        if x == self.__curBlockX and y == self.__curBlockY and z == self.__curBlockZ:
            block = self._mc.theWorld.getBlockId(x, y, z)
            if block == 0:
                return

            block = blocks.blocksList[block]
            self.__prevBlockDamage = block.blockStrength(self._mc.thePlayer)
            if self.__curBlockDamage % 4 == 0 and block:
                speed = (block.stepSound.soundVolume + 1.0) / 8.0
                self._mc.sndManager.playSound(
                    f'step.{block.stepSound.soundDir}', x + 0.5, y + 0.5, z + 0.5,
                    speed, block.stepSound.soundPitch * 0.5
                )

            self.__curBlockDamage += 1
            if self.__curBlockDamage == self.__prevBlockDamage + 1:
                self.sendBlockRemoved(x, y, z)
                self.__curBlockDamage = 0
                self.__blockHitWait = 5
        else:
            self.__curBlockDamage = 0
            self.__curBlockX = x
            self.__curBlockY = y
            self.__curBlockZ = z

    def setPartialTime(self, damageTime):
        if self.__curBlockDamage <= 0:
            self._mc.renderGlobal.damagePartialTime = 0.0
        else:
            self._mc.renderGlobal.damagePartialTime = (self.__curBlockDamage + damageTime - 1.0) / self.__prevBlockDamage

    def getBlockReachDistance(self):
        return 4.0

    def onWorldChange(self, world):
        super().onWorldChange(world)

        self.__mobSpawner = MobSpawner(world)
        size = world.width * world.length * world.height // 64 // 64 // 64
        for i in range(size):
            self.__mobSpawner.spawnMob(size, world.playerEntity, None)

    def onUpdate(self):
        self.__mobSpawner.spawnMobs()
