from mc.net.minecraft.User import User
from mc.net.minecraft.gamemode.GameMode import GameMode
from mc.net.minecraft.gui.BlockSelectionScreen import BlockSelectionScreen

class CreativeGameMode(GameMode):

    def __init__(self, minecraft):
        super().__init__(minecraft)
        self.mode = True

    def handleOpenInventory(self):
        self._minecraft.setScreen(BlockSelectionScreen())

    def initLevel(self, level):
        super().initLevel(level)
        level.removeAllNonCreativeModeEntities()
        level.creativeMode = True
        level.growTrees = False

    def adjustPlayer(self, player):
        for i in range(9):
            player.inventory.count[i] = 1
            if player.inventory.slots[i] <= 0:
                player.inventory.slots[i] = User.creativeTiles[i].id

    def canHurtPlayer(self):
        return False
