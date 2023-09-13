from mc.net.minecraft.gamemode.GameMode import GameMode
from mc.net.minecraft.level.MobSpawner import MobSpawner
from mc.net.minecraft.level.tile.Tiles import tiles
from mc.net.minecraft.mob.Mob import Mob

class SurvivalGameMode(GameMode):

    def __init__(self, minecraft):
        super().__init__(minecraft)
        self.__x = 0
        self.__y = 0
        self.__z = 0
        self.__oDestroyProgress = 0
        self.__destroyProgress = 0
        self.__delay = 0
        self.__mobSpawner = None

    def initPlayer(self, player):
        player.inventory.slots[8] = tiles.tnt.id
        player.inventory.count[8] = 10

    def destroyBlock(self, x, y, z):
        tile = self._minecraft.level.getTile(x, y, z)
        tiles.tiles[tile].spawnResources(self._minecraft.level, x, y, z)
        super().destroyBlock(x, y, z)

    def consumeBlock(self, tile):
        return self._minecraft.player.inventory.removeResource(tile)

    def startDestroyBlock(self, x, y, z):
        tile = self._minecraft.level.getTile(x, y, z)
        if tile > 0 and tiles.tiles[tile].getDestroyProgress() == 0:
            self.destroyBlock(x, y, z)

    def stopDestroyBlock(self):
        self.__oDestroyProgress = 0
        self.__delay = 0

    def continueDestroyBlock(self, x, y, z, sideHit):
        if self.__delay > 0:
            self.__delay -= 1
            return

        if x == self.__x and y == self.__y and z == self.__z:
            tile = self._minecraft.level.getTile(x, y, z)
            if tile == 0:
                return

            block = tiles.tiles[tile]
            self.__destroyProgress = block.getDestroyProgress()
            block.addParticleOnBlockBreaking(self._minecraft.level, x, y, z, sideHit, self._minecraft.particleEngine)
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
            self._minecraft.levelRenderer.hurtTime = 0.0
        else:
            self._minecraft.levelRenderer.hurtTime = (self.__oDestroyProgress + damageTime - 1.0) / self.__destroyProgress

    def getPickRange(self):
        return 4.0

    def removeResource(self, entity, quantity):
        tile = tiles.tiles[quantity]
        if tile == tiles.mushroomRed and self._minecraft.player.inventory.removeResource(quantity):
            entity.hurt(None, 3)
            return True
        elif tile == tiles.mushroomBrown and self._minecraft.player.inventory.removeResource(quantity):
            entity.heal(5)
            return True

        return False

    def initLevel(self, level):
        super().initLevel(level)
        self.__mobSpawner = MobSpawner(level)

    def tick(self):
        size = self.__mobSpawner.level.width * self.__mobSpawner.level.height * self.__mobSpawner.level.depth // 64 // 64 // 64
        if int(self.__mobSpawner.level.rand.random() * 100) < size and \
           self.__mobSpawner.level.countInstanceOf(Mob) < size * 20:
            self.__mobSpawner.spawnMobs(size, self.__mobSpawner.level.player, None)

    def createPlayer(self, level):
        self.__mobSpawner = MobSpawner(level)
        self._minecraft.loadingScreen.levelLoadUpdate('Spawning..')
        size = level.width * level.height * level.depth // 800
        self.__mobSpawner.spawnMobs(size, None, self._minecraft.loadingScreen)
