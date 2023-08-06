from mc.net.minecraft.phys.AABB import AABB

import random
import math

class Entity:
    xo = 0.0
    yo = 0.0
    zo = 0.0
    xd = 0.0
    yd = 0.0
    zd = 0.0
    yRot = 0.0
    xRot = 0.0
    yRotO = 0.0
    xRotO = 0.0
    onGround = False

    removed = False
    heightOffset = 0.0

    bbWidth = 0.6
    bbHeight = 1.8

    def __init__(self, level):
        self.level = level
        self.resetPos()

    def resetPos(self):
        x = random.random() * self.level.width
        y = self.level.depth + 10
        z = random.random() * self.level.height
        self.setPos(x, y, z)

    def remove(self):
        self.removed = True

    def setSize(self, w, h):
        self.bbWidth = w
        self.bbHeight = h

    def setPos(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        w = self.bbWidth / 2.0
        h = self.bbHeight / 2.0
        self.bb = AABB(x - w, y - h, z - w, x + w, y + h, z + w)

    def turn(self, xo, yo):
        orgXRot = self.xRot
        orgYRot = self.yRot
        self.yRot = self.yRot + xo * 0.15
        self.xRot = self.xRot - yo * 0.15
        if self.xRot < -90.0:
            self.xRot = -90.0
        if self.xRot > 90.0:
            self.xRot = 90.0

        self.xRotO += self.xRot - orgXRot
        self.yRotO += self.yRot - orgYRot

    def tick(self):
        self.xo = self.x
        self.yo = self.y
        self.zo = self.z

    def move(self, xa, ya, za):
        xaOrg = xa
        yaOrg = ya
        zaOrg = za

        aABBs = self.level.getCubes(self.bb.expand(xa, ya, za))
        for aABB in aABBs:
            ya = aABB.clipYCollide(self.bb, ya)

        self.bb.move(0.0, ya, 0.0)

        for aABB in aABBs:
            xa = aABB.clipXCollide(self.bb, xa)

        self.bb.move(xa, 0.0, 0.0)

        for aABB in aABBs:
            za = aABB.clipZCollide(self.bb, za)

        self.bb.move(0.0, 0.0, za)

        self.onGround = yaOrg != ya and yaOrg < 0.0

        if xaOrg != xa:
            self.xd = 0.0
        if yaOrg != ya:
            self.yd = 0.0
        if zaOrg != za:
            self.zd = 0.0

        self.x = (self.bb.x0 + self.bb.x1) / 2.0
        self.y = self.bb.y0 + self.heightOffset
        self.z = (self.bb.z0 + self.bb.z1) / 2.0

    def moveRelative(self, xa, za, speed):
        dist = xa * xa + za * za
        if dist < 0.01:
            return

        dist = speed / math.sqrt(dist)
        xa *= dist
        za *= dist

        sin = math.sin(self.yRot * math.pi / 180.0)
        cos = math.cos(self.yRot * math.pi / 180.0)

        self.xd += xa * cos - za * sin
        self.zd += za * cos + xa * sin

    def isLit(self):
        return self.level.isLit(self.x, self.y, self.z)
