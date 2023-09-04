class HitResult:

    def __init__(self, x, y=None, z=None, sideHit=None, hitVec=None):
        if y is None:
            entity = x
            self.typeOfHit = 1
            self.entity = x
            self.x = 0
            self.y = 0
            self.z = 0
            self.sideHit = 0
            self.vec = None
        else:
            self.typeOfHit = 0
            self.x = x
            self.y = y
            self.z = z
            self.sideHit = sideHit
            self.vec = hitVec
            self.entity = None
