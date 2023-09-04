from mc.net.minecraft.player.Inventory import Inventory
from mc.net.minecraft.player.PlayerInput import PlayerInput
from mc.net.minecraft.model.PlayerModel import PlayerModel
from mc.net.minecraft.mob.Mob import Mob

import math

class Player(Mob):
    MAX_HEALTH = 20

    def __init__(self, level, keyboardInput):
        super().__init__(level)
        level.player = self
        level.removeEntity(self)
        level.addEntity(self)
        print(level.player)
        self.heightOffset = 1.62
        self.__input = keyboardInput
        self.inventory = Inventory()
        self.health = Player.MAX_HEALTH
        self.model = PlayerModel()
        self.rotOffs = 180.0
        self.ai = PlayerInput(self, keyboardInput)
        self.userType = 0
        self.oBob = 0.0
        self.bob = 0.0
        self.score = 0

    def resetPos(self):
        self.heightOffset = 1.62
        self.setSize(0.6, 1.8)
        super().resetPos()
        self.level.player = self
        self.health = Player.MAX_HEALTH
        self.deathTime = 0

    def aiStep(self):
        for i in range(len(self.inventory.popTime)):
            if self.inventory.popTime[i] <= 0:
                continue

            self.inventory.popTime[i] = self.inventory.popTime[i] - 1

        self.oBob = self.bob
        self.__input.tick()
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
        if entities:
            for entity in entities:
                entity.playerTouch(self)

    def render(self, textures, translation):
        pass

    def releaseAllKeys(self):
        self.__input.releaseAllKeys()

    def setKey(self, symbol, state):
        self.__input.setKey(symbol, state)

    def addResource(self, index):
        slot = self.inventory.containsTileAt(index)
        if slot < 0:
            slot = self.inventory.containsTileAt(-1)

        if slot < 0:
            return False
        elif self.inventory.count[slot] >= 99:
            return False

        self.inventory.slots[slot] = index
        self.inventory.count[slot] += 1
        self.inventory.popTime[slot] = 5
        return True

    def getScore(self):
        return self.score

    def getModel(self):
        return self.model

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
