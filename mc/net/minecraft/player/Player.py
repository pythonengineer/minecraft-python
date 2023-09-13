from mc.net.minecraft.player.Inventory import Inventory
from mc.net.minecraft.player.PlayerInput import PlayerInput
from mc.net.minecraft.mob.Mob import Mob
from pyglet import gl

import math

class Player(Mob):
    MAX_HEALTH = 20
    MAX_ARROWS = 99
    __texture = -1
    newTexture = None

    def __init__(self, level):
        super().__init__(level)
        if level:
            level.player = self
            level.removeEntity(self)
            level.addEntity(self)

        self.heightOffset = 1.62
        self.input = None
        self.inventory = Inventory()
        self.health = Player.MAX_HEALTH
        self.modelName = 'humanoid'
        self.rotOffs = 180.0
        self.ai = PlayerInput(self)
        self.userType = 0
        self.oBob = 0.0
        self.bob = 0.0
        self.score = 0
        self.arrows = 20

    def resetPos(self):
        self.heightOffset = 1.62
        self.setSize(0.6, 1.8)
        super().resetPos()
        if self.level:
            self.level.player = self

        self.health = Player.MAX_HEALTH
        self.deathTime = 0

    def aiStep(self):
        self.inventory.tick()
        self.oBob = self.bob
        self.input.tick()
        super().aiStep()

        d = math.sqrt(self.xd * self.xd + self.zd * self.zd)
        t = math.atan(-self.yd * 0.2) * 15.0
        if d > 0.1:
            d = 0.1
        if not self.onGround or self.health <= 0:
            d = 0.0
        if self.onGround or self.health <= 0:
            t = 0.0

        self.bob += (d - self.bob) * 0.4
        self.tilt += (t - self.tilt) * 0.8
        entities = self.level.findEntities(self, self.bb.grow(1.0, 0.0, 1.0))
        if self.health > 0 and entities:
            for entity in entities:
                entity.playerTouch(self)

    def render(self, textures, translation):
        pass

    def releaseAllKeys(self):
        self.input.releaseAllKeys()

    def setKey(self, symbol, state):
        self.input.setKey(symbol, state)

    def addResource(self, index):
        return self.inventory.addResource(index)

    def getScore(self):
        return self.score

    def getModel(self):
        return self.modelCache.getModel(self.modelName)

    def die(self, entity):
        self.setSize(0.2, 0.2)
        self.setPos(self.x, self.y, self.z)
        self.yd = 0.1
        if entity:
            self.xd = -(math.cos((self.hurtDir + self.yRot) * math.pi / 180.0)) * 0.1
            self.zd = -(math.sin((self.hurtDir + self.yRot) * math.pi / 180.0)) * 0.1
        else:
            self.zd = 0.0
            self.xd = 0.0

        self.heightOffset = 0.1

    def remove(self):
        pass

    def awardKillScore(self, entity, score):
        self.score += score

    def isShootable(self):
        return True

    def bindTexture(self, textures):
        if self.newTexture:
            self.__texture = textures.loadTextureImg(self.newTexture)
            self.newTexture = None

        if self.__texture < 0:
            gl.glBindTexture(gl.GL_TEXTURE_2D, textures.loadTexture('char.png'))
        else:
            gl.glBindTexture(gl.GL_TEXTURE_2D, self.__texture)

    def hurt(self, entity, hp):
        if not self.level.creativeMode:
            super().hurt(entity, hp)

    def isCreativeModeAllowed(self):
        return True
