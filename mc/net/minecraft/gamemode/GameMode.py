from mc.net.minecraft.level.tile.Tiles import SoundType, tiles

class GameMode:

    def __init__(self, minecraft):
        self._minecraft = minecraft
        self.mode = False

    def initLevel(self, level):
        level.creativeMode = False

    def handleOpenInventory(self):
        pass

    def startDestroyBlock(self, x, y, z):
        self.destroyBlock(x, y, z)

    def consumeBlock(self, tile):
        return True

    def destroyBlock(self, x, y, z):
        tile = tiles.tiles[self._minecraft.level.getTile(x, y, z)]
        change = self._minecraft.level.netSetTile(x, y, z, 0)
        if tile and change:
            if self._minecraft.isOnlineClient():
                self._minecraft.networkClient.sendTileUpdated(x, y, z, 0,
                                                              self._minecraft.player.inventory.getSelected())
            if tile.soundType != SoundType.none:
                self._minecraft.level.playSound('step.' + tile.soundType.soundName,
                                         x, y, z,
                                         (tile.soundType.getVolume() + 1.0) / 2.0,
                                         tile.soundType.getPitch() * 0.8)

            tile.destroy(self._minecraft.level, x, y, z, self._minecraft.particleEngine)

    def continueDestroyBlock(self, x, y, z, sideHit):
        pass

    def stopDestroyBlock(self):
        pass

    def render(self, damageTime):
        pass

    def getPickRange(self):
        return 5.0

    def removeResource(self, player, quantity):
        return False

    def initPlayer(self, player):
        pass

    def tick(self):
        pass

    def createPlayer(self, level):
        pass

    def canHurtPlayer(self):
        return True

    def adjustPlayer(self, player):
        pass
