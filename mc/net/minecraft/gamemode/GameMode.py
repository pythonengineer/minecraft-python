from mc.net.minecraft.level.tile.Tiles import SoundType, tiles

class GameMode:

    def __init__(self, minecraft):
        self._mc = minecraft
        self.isInTestMode = False

    def startDestroyBlock(self, x, y, z):
        self.destroyBlock(x, y, z)

    def consumeBlock(self, tile):
        return True

    def destroyBlock(self, x, y, z):
        tile = tiles.tiles[self._mc.level.getTile(x, y, z)]
        change = self._mc.level.netSetTile(x, y, z, 0)
        if tile and change:
            if self._mc.isOnlineClient():
                self._mc.networkClient.sendTileUpdated(x, y, z, 0, self._mc.player.inventory.getSelected())
            if tile.soundType != SoundType.none:
                self._mc.level.playSound('step.' + tile.soundType.soundName,
                                         x, y, z,
                                         (tile.soundType.getVolume() + 1.0) / 2.0,
                                         tile.soundType.getPitch() * 0.8)

            tile.destroy(self._mc.level, x, y, z, self._mc.particleEngine)

    def stopDestroyingBlock(self, x, y, z, sideHit):
        pass

    def tick(self):
        pass

    def render(self, damageTime):
        pass

    def getPickRange(self):
        return 5.0

    def removeResource(self, player, quantity):
        return False
