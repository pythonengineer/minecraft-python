from mc.net.minecraft.Entity import Entity

class Player(Entity):
    upPressed = False
    downPressed = False
    leftPressed = False
    rightPressed = False
    spacePressed = False

    def __init__(self, level):
        super().__init__(level)
        self.heightOffset = 1.62

    def tick(self):
        self.xo = self.x
        self.yo = self.y
        self.zo = self.z
        xa = 0.0
        ya = 0.0

        if self.upPressed: ya -= 1.0
        if self.downPressed: ya += 1.0
        if self.leftPressed: xa -= 1.0
        if self.rightPressed: xa += 1.0
        if self.spacePressed:
            if self.onGround:
                self.yd = 0.12

        self.moveRelative(xa, ya, 0.02 if self.onGround else 0.005)

        self.yd -= 0.005
        self.move(self.xd, self.yd, self.zd)
        self.xd *= 0.91
        self.yd *= 0.98
        self.zd *= 0.91

        if self.onGround:
            self.xd *= 0.8
            self.zd *= 0.8
