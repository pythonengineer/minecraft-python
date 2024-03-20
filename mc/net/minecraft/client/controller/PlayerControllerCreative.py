from mc.net.minecraft.client.Session import Session
from mc.net.minecraft.client.controller.PlayerController import PlayerController
from mc.net.minecraft.client.gui.GuiInventory import GuiInventory
from mc.net.minecraft.game.entity.player.ItemStack import ItemStack
from mc.net.minecraft.game.level.MobSpawner import MobSpawner
from mc.net.minecraft.game.level.block.Blocks import blocks

class PlayerControllerCreative(PlayerController):

    def displayInventoryGUI(self):
        self._mc.displayGuiScreen(GuiInventory())

    def flipPlayer(self, player):
        for i in range(9):
            if player.inventory.mainInventory[i] is None:
                player.inventory.mainInventory[i] = ItemStack(blocks.blocksList[Session.allowedBlocks[i].blockID])
            else:
                player.inventory.mainInventory[i].stackSize = 1

    def shouldDrawHUD(self):
        return False

    def onWorldChange(self, world):
        super().onWorldChange(world)
        world.survivalWorld = False

        self.__mobSpawner = MobSpawner(world)
        size = world.width * world.length * world.height // 64 // 64 // 64
        for i in range(size):
            self.__mobSpawner.performSpawning(size, world.playerEntity, None)

    def onUpdate(self):
        self.__mobSpawner.spawn()
