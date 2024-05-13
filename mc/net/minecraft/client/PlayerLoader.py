from mc.net.minecraft.client.player.EntityPlayerSP import EntityPlayerSP
from mc.net.minecraft.game.level.LevelLoader import LevelLoader

class PlayerLoader(LevelLoader):

    def __init__(self, minecraft, loadingScreen):
        super().__init__(loadingScreen)
        self.__minecraft = minecraft

    def _loadEntity(self, world, entityId):
        if entityId == 'LocalPlayer':
            return EntityPlayerSP(self.__minecraft, world)
        else:
            super()._loadEntity(world, entityId)
