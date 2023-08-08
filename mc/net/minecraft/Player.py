from mc.net.minecraft.Entity import Entity
from pyglet import window

class Player(Entity):
    keys = [False] * 10

    def __init__(self, level):
        super().__init__(level)
        self.heightOffset = 1.62

    def setKey(self, key, state):
        id_ = -1
        if key in (window.key.UP, window.key.W): id_ = 0
        if key in (window.key.DOWN, window.key.S): id_ = 1
        if key in (window.key.LEFT, window.key.A): id_ = 2
        if key in (window.key.RIGHT, window.key.D): id_ = 3
        if key in (window.key.SPACE, window.key.LWINDOWS, window.key.LMETA): id_ = 4
        if id_ >= 0:
            self.keys[id_] = state

    def releaseAllKeys(self):
        for i in range(10):
            self.keys[i] = False

    def tick(self):
        self.xo = self.x
        self.yo = self.y
        self.zo = self.z
        xa = 0.0
        ya = 0.0

        inWater = self.isInWater()
        inLava = self.isInLava()

        if self.keys[0]: ya -= 1.0
        if self.keys[1]: ya += 1.0
        if self.keys[2]: xa -= 1.0
        if self.keys[3]: xa += 1.0
        if self.keys[4]:
            if inWater:
                self.yd += 0.04
            elif inLava:
                self.yd += 0.04
            elif self.onGround:
                self.yd = 0.42
                self.keys[4] = False

        if inWater:
            yo = self.y
            self.moveRelative(xa, ya, 0.02)
            self.move(self.xd, self.yd, self.zd)
            self.xd *= 0.8
            self.yd *= 0.8
            self.zd *= 0.8
            self.yd -= 0.02

            if self.horizontalCollision and self.isFree(self.xd, self.yd + 0.6 - self.y + yo, self.zd):
                self.yd = 0.3
        elif inLava:
            yo = self.y
            self.moveRelative(xa, ya, 0.02)
            self.move(self.xd, self.yd, self.zd)
            self.xd *= 0.5
            self.yd *= 0.5
            self.zd *= 0.5
            self.yd -= 0.02

            if self.horizontalCollision and self.isFree(self.xd, self.yd + 0.6 - self.y + yo, self.zd):
                self.yd = 0.3
        else:
            self.moveRelative(xa, ya, 0.1 if self.onGround else 0.02)
            self.move(self.xd, self.yd, self.zd)
            self.xd *= 0.91
            self.yd *= 0.98
            self.zd *= 0.91
            self.yd -= 0.08

            if self.onGround:
                self.xd *= 0.6
                self.zd *= 0.6
