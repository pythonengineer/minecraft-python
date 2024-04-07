from mc.net.minecraft.client.controller.PlayerController import PlayerController
from mc.net.minecraft.client.gui.GuiInventory import GuiInventory
from mc.net.minecraft.game.level.MobSpawner import MobSpawner
from mc.net.minecraft.game.level.block.Blocks import blocks
from mc.net.minecraft.game.entity.EntityLiving import EntityLiving
from mc.net.minecraft.game.entity.player.ItemStack import ItemStack

class PlayerControllerSP(PlayerController):

    def __init__(self, mc):
        super().__init__(mc)
        self.__hitX = -1
        self.__hitY = -1
        self.__hitZ = -1
        self.__hits = 0
        self.__hardness = 0
        self.__hitDelay = 0
        self.__mobSpawner = None

    def displayInventoryGUI(self):
        self._mc.displayGuiScreen(GuiInventory())

    def onRespawn(self, player):
        player.inventory.mainInventory[6] = ItemStack(blocks.torch, 99)
        player.inventory.mainInventory[7] = ItemStack(blocks.tnt, 99)
        player.inventory.mainInventory[8] = ItemStack(blocks.bookshelf, 99)

        for i in range(20):
            row = i % 5
            col = i // 5
            player.inventory.mainInventory[i + 9] = ItemStack(row + (col << 4), 1)

    def sendBlockRemoved(self, x, y, z):
        block = self._mc.theWorld.getBlockId(x, y, z)
        blocks.blocksList[block].dropBlockAsItem(self._mc.theWorld, x, y, z)
        super().sendBlockRemoved(x, y, z)

    def canPlace(self, x, y, z, block):
        super().canPlace(x, y, z, block)
        return self._mc.thePlayer.inventory.removeResource(block)

    def clickBlock(self, x, y, z):
        block = self._mc.theWorld.getBlockId(x, y, z)
        if block > 0 and blocks.blocksList[block].blockStrength() == 0:
            self.sendBlockRemoved(x, y, z)

    def resetBlockRemoving(self):
        self.__hits = 0
        self.__hitDelay = 0

    def hitBlock(self, x, y, z, sideHit):
        if self.__hitDelay > 0:
            self.__hitDelay -= 1
            return

        super().hitBlock(x, y, z, sideHit)
        if x == self.__hitX and y == self.__hitY and z == self.__hitZ:
            block = self._mc.theWorld.getBlockId(x, y, z)
            if block == 0:
                return

            block = blocks.blocksList[block]
            self.__hardness = block.blockStrength()
            if self.__hits % 4 == 0 and block:
                speed = (block.stepSound.speed + 1.0) / 8.0
                self._mc.sndManager.playSoundAtPos(
                    f'step.{block.stepSound.name}', x + 0.5, y + 0.5, z + 0.5,
                    speed, block.stepSound.pitch * 0.5
                )

            self.__hits += 1
            if self.__hits == self.__hardness + 1:
                self.sendBlockRemoved(x, y, z)
                self.__hits = 0
                self.__hitDelay = 5
        else:
            self.__hits = 0
            self.__hitX = x
            self.__hitY = y
            self.__hitZ = z

    def setPartialTime(self, damageTime):
        if self.__hits <= 0:
            self._mc.renderGlobal.damagePartialTime = 0.0
        else:
            self._mc.renderGlobal.damagePartialTime = (self.__hits + damageTime - 1.0) / self.__hardness

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
