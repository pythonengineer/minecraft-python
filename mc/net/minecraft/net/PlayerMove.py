class PlayerMove:

    def __init__(self, x, y, z=None, yRot=None, xRot=None):
        if z is None:
            self.yRot = x
            self.xRot = y
            self.rotating = True
            self.moving = False
            return
        elif yRot is None:
            self.moving = True
            self.rotating = False
        else:
            self.yRot = yRot
            self.xRot = xRot
            self.rotating = True
            self.moving = True

        self.x = x
        self.y = y
        self.z = z
