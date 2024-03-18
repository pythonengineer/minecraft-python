from mc.net.minecraft.client.Session import Session
from mc.net.minecraft.client.controller.PlayerController import PlayerController
from mc.net.minecraft.client.gui.GuiCreativeInventory import GuiCreativeInventory
from mc.net.minecraft.game.level.MobSpawner import MobSpawner

class PlayerControllerCreative(PlayerController):

    def __init__(self, mc):
        super().__init__(mc)
        self.isInTestMode = True

    def displayInventoryGUI(self):
        self._mc.displayGuiScreen(GuiCreativeInventory())

    def flipPlayer(self, player):
        for i in range(9):
            player.inventory.stackSize[i] = 1
            if player.inventory.mainInventory[i] <= 0:
                player.inventory.mainInventory[i] = Session.allowedBlocks[i].blockID

    def shouldDrawHUD(self):
        return False

    def onWorldChange(self, world):
        super().onWorldChange(world)
        world.survivalWorld = False

        self.__mobSpawner = MobSpawner(world)
        size = world.width * world.length * world.height // 64 // 64 // 8
        for i in range(size):
            self.__mobSpawner.performSpawning(size, world.playerEntity, None)

    def onUpdate(self):
        self.__mobSpawner.spawn()
