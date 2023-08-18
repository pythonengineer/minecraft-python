from mc.net.minecraft.player.Inventory import Inventory
from mc.net.minecraft.Entity import Entity

class Player(Entity):

    def __init__(self, level, movementInput):
        super().__init__(level)
        self.heightOffset = 1.62
        self.__input = movementInput
        self.inventory = Inventory()
        self.userType = 0

    def tick(self):
        super().tick()
        inWater = self.isInWater()
        inLava = self.isInLava()
        self.__input.updatePlayerMoveState()
        if self.__input.jumpHeld:
            if inWater:
                self.yd += 0.04
            elif inLava:
                self.yd += 0.04
            elif self.onGround and not self.__input.jump:
                self.yd = 0.42
                self.__input.jump = True
        else:
            self.__input.jump = False

        if inWater:
            yo = self.y
            self.moveRelative(self.__input.moveStrafe, self.__input.moveForward, 0.02)
            self.move(self.xd, self.yd, self.zd)
            self.xd *= 0.8
            self.yd *= 0.8
            self.zd *= 0.8
            self.yd -= 0.02
            if self.horizontalCollision and self.isFree(self.xd, self.yd + 0.6 - self.y + yo, self.zd):
                self.yd = 0.3
        elif inLava:
            yo = self.y
            self.moveRelative(self.__input.moveStrafe, self.__input.moveForward, 0.02)
            self.move(self.xd, self.yd, self.zd)
            self.xd *= 0.5
            self.yd *= 0.5
            self.zd *= 0.5
            self.yd -= 0.02
            if self.horizontalCollision and self.isFree(self.xd, self.yd + 0.6 - self.y + yo, self.zd):
                self.yd = 0.3
        else:
            self.moveRelative(self.__input.moveStrafe, self.__input.moveForward, 0.1 if self.onGround else 0.02)
            self.move(self.xd, self.yd, self.zd)
            self.xd *= 0.91
            self.yd *= 0.98
            self.zd *= 0.91
            self.yd -= 0.08
            if self.onGround:
                self.xd *= 0.6
                self.zd *= 0.6

    def releaseAllKeys(self):
        self.__input.releaseAllKeys()

    def setKey(self, symbol, state):
        self.__input.setKey(symbol, state)
