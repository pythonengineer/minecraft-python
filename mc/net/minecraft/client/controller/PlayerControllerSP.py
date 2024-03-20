from mc.net.minecraft.client.controller.PlayerController import PlayerController
from mc.net.minecraft.client.gui.GuiInventory import GuiInventory
from mc.net.minecraft.game.level.MobSpawner import MobSpawner
from mc.net.minecraft.game.level.block.Blocks import blocks
from mc.net.minecraft.game.entity.EntityLiving import EntityLiving
from mc.net.minecraft.game.entity.player.ItemStack import ItemStack

class PlayerControllerSP(PlayerController):

    def __init__(self, mc):
        super().__init__(mc)
        self.__curBlockX = -1
        self.__curBlockY = -1
        self.__curBlockZ = -1
        self.__curBlockProgress = 0
        self.__prevBlockProgress = 0
        self.__blockHitWait = 0
        self.__mobSpawner = None

    def displayInventoryGUI(self):
        self._mc.displayGuiScreen(GuiInventory())

    def preparePlayer(self, player):
        player.inventory.mainInventory[8] = ItemStack(blocks.bookShelf, 99)
        player.inventory.mainInventory[7] = ItemStack(blocks.tnt, 99)

        for i in range(20):
            row = i % 5
            col = i // 5
            player.inventory.mainInventory[i + 9] = ItemStack(row + (col << 4))

    def sendBlockRemoved(self, x, y, z):
        block = self._mc.theWorld.getBlockId(x, y, z)
        blocks.blocksList[block].dropBlockAsItem(self._mc.theWorld, x, y, z)
        super().sendBlockRemoved(x, y, z)

    def canPlace(self, block):
        return self._mc.thePlayer.inventory.consumeInventoryItem(block)

    def clickBlock(self, x, y, z):
        block = self._mc.theWorld.getBlockId(x, y, z)
        if block > 0 and blocks.blocksList[block].blockStrength() == 0:
            self.sendBlockRemoved(x, y, z)

    def resetBlockRemoving(self):
        self.__curBlockProgress = 0
        self.__blockHitWait = 0

    def sendBlockRemoving(self, x, y, z):
        if self.__blockHitWait > 0:
            self.__blockHitWait -= 1
            return

        if x == self.__curBlockX and y == self.__curBlockY and z == self.__curBlockZ:
            block = self._mc.theWorld.getBlockId(x, y, z)
            if block == 0:
                return

            block = blocks.blocksList[block]
            self.__prevBlockProgress = block.blockStrength()
            self.__curBlockProgress += 1
            if self.__curBlockProgress == self.__prevBlockProgress + 1:
                self.sendBlockRemoved(x, y, z)
                self.__curBlockProgress = 0
                self.__blockHitWait = 5
        else:
            self.__curBlockProgress = 0
            self.__curBlockX = x
            self.__curBlockY = y
            self.__curBlockZ = z

    def setPartialTime(self, damageTime):
        if self.__curBlockProgress <= 0:
            self._mc.renderGlobal.damagePartialTime = 0.0
        else:
            self._mc.renderGlobal.damagePartialTime = (self.__curBlockProgress + damageTime - 1.0) / self.__prevBlockProgress

    def getBlockReachDistance(self):
        return 4.0

    def onWorldChange(self, world):
        super().onWorldChange(world)

        self.__mobSpawner = MobSpawner(world)
        size = world.width * world.length * world.height // 64 // 64 // 8
        for i in range(size):
            self.__mobSpawner.performSpawning(size, world.playerEntity, None)

    def onUpdate(self):
        self.__mobSpawner.spawn()
