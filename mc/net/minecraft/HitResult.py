class HitResult:

    def __init__(self, type_, x, y, z, f):
        self.x = x
        self.y = y
        self.z = z
        self.f = f

    def isCloserThan(self, player, o, editMode):
        dist = self.__distanceTo(player, 0)
        dist2 = o.__distanceTo(player, 0)
        if dist < dist2:
            return True
        dist = self.__distanceTo(player, editMode)
        dist2 = o.__distanceTo(player, editMode)
        if dist < dist2:
            return True
        return False

    def __distanceTo(self, player, editMode):
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
