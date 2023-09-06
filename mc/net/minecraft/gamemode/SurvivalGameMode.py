from mc.net.minecraft.gamemode.GameMode import GameMode
from mc.net.minecraft.level.tile.Tiles import tiles

class SurvivalGameMode(GameMode):

    def __init__(self, minecraft):
        super().__init__(minecraft)
        self.__x = -1
        self.__y = -1
        self.__z = -1
        self.__oDestroyProgress = 0
        self.__destroyProgress = 0
        self.__delay = 0

    def destroyBlock(self, x, y, z):
        tile = self._mc.level.getTile(x, y, z)
        tiles.tiles[tile].spawnResources(self._mc.level, x, y, z)
        super().destroyBlock(x, y, z)

    def consumeBlock(self, tile):
        return self._mc.player.inventory.removeResource(tile)

    def startDestroyBlock(self, x, y, z):
        tile = self._mc.level.getTile(x, y, z)
        if tile > 0 and tiles.tiles[tile].getDestroyProgress() == 0:
            self.destroyBlock(x, y, z)

    def tick(self):
        self.__oDestroyProgress = 0
        self.__delay = 0

    def stopDestroyingBlock(self, x, y, z, sideHit):
        if self.__delay > 0:
            self.__delay -= 1
            return

        if x == self.__x and y == self.__y and z == self.__z:
            tile = self._mc.level.getTile(x, y, z)
            if tile == 0:
                return

            block = tiles.tiles[tile]
            self.__destroyProgress = block.getDestroyProgress()
            block.addParticleOnBlockBreaking(self._mc.level, x, y, z, sideHit, self._mc.particleEngine)
            self.__oDestroyProgress += 1
            if self.__oDestroyProgress == self.__destroyProgress + 1:
                self.destroyBlock(x, y, z)
                self.__oDestroyProgress = 0
                self.__delay = 5
            return

        self.__oDestroyProgress = 0
        self.__x = x
        self.__y = y
        self.__z = z

    def render(self, damageTime):
        if self.__oDestroyProgress <= 0:
            self._mc.levelRenderer.hurtTime = 0.0
        else:
            self._mc.levelRenderer.hurtTime = (self.__oDestroyProgress + damageTime - 1.0) / self.__destroyProgress

    def getPickRange(self):
        return 4.0

    def removeResource(self, entity, quantity):
        tile = tiles.tiles[quantity]
        if tile == tiles.mushroomRed and self._mc.player.inventory.removeResource(quantity):
            entity.hurt(None, 3)
            return True
        elif tile == tiles.mushroomBrown and self._mc.player.inventory.removeResource(quantity):
            entity.heal(5)
            return True

        return False
