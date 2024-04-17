from mc.net.minecraft.client.controller.PlayerController import PlayerController
from mc.net.minecraft.client.gui.GuiInventory import GuiInventory
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

    def openInventory(self):
        self._mc.displayGuiScreen(GuiInventory())

    def flipPlayer(self, player):
        player.inventory.mainInventory[4] = ItemStack(blocks.clothWhite, 99)
        player.inventory.mainInventory[5] = ItemStack(blocks.glass, 99)
        player.inventory.mainInventory[6] = ItemStack(blocks.torch, 99)
        player.inventory.mainInventory[7] = ItemStack(blocks.tnt, 99)
        player.inventory.mainInventory[8] = ItemStack(blocks.bookShelf, 99)

        slot = 0
        for i in range(256, 1024):
            if items.itemsList[i]:
                player.inventory.mainInventory[slot] = ItemStack(i)
                slot += 1

            if slot >= 4:
                break

        player.inventory.mainInventory[9] = ItemStack(items.apple.shiftedIndex, 99)

    def sendBlockRemoved(self, x, y, z):
        block = self._mc.theWorld.getBlockId(x, y, z)
        change = super().sendBlockRemoved(x, y, z)
        if change:
            blocks.blocksList[block].dropBlockAsItem(self._mc.theWorld, x, y, z)

        return change

    def clickBlock(self, x, y, z):
        block = self._mc.theWorld.getBlockId(x, y, z)
        if block > 0 and blocks.blocksList[block].blockStrength(self._mc.thePlayer) == 0:
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
            self.__mobSpawner.performSpawning(size, world.playerEntity, None)

    def onUpdate(self):
        self.__mobSpawner.spawn()
