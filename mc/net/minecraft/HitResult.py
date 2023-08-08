class HitResult:

    def __init__(self, type_, x, y, z, f):
        self.x = x
        self.y = y
        self.z = z
        self.f = f

    def distanceTo(self, player, editMode):
        xx = self.x
        yy = self.y
        zz = self.z
        if editMode == 1:
            if self.f == 0: yy -= 1
            elif self.f == 1: yy += 1
            elif self.f == 2: zz -= 1
            elif self.f == 3: zz += 1
            elif self.f == 4: xx -= 1
            elif self.f == 5: xx == 1
        xd = xx - player.x
        yd = yy - player.y
        zd = zz - player.z
        return xd * xd + yd * yd + zd * zd
