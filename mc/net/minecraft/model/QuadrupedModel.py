from mc.net.minecraft.model.BaseModel import BaseModel
from mc.net.minecraft.model.Cube import Cube

import math

class QuadrupedModel(BaseModel):

    def __init__(self, size, scale):
        self.head = Cube(0, 0)
        self.head.addBox(-4.0, -4.0, -8.0, 8, 8, 8, 0.0)
        self.head.setPos(0.0, 18 - size, -6.0)
        self.body = Cube(28, 8)
        self.body.addBox(-5.0, -10.0, -7.0, 10, 16, 8, 0.0)
        self.body.setPos(0.0, 17 - size, 2.0)
        self.leg1 = Cube(0, 16)
        self.leg1.addBox(-2.0, 0.0, -2.0, 4, size, 4, 0.0)
        self.leg1.setPos(-3.0, 24 - size, 7.0)
        self.leg2 = Cube(0, 16)
        self.leg2.addBox(-2.0, 0.0, -2.0, 4, size, 4, 0.0)
        self.leg2.setPos(3.0, 24 - size, 7.0)
        self.leg3 = Cube(0, 16)
        self.leg3.addBox(-2.0, 0.0, -2.0, 4, size, 4, 0.0)
        self.leg3.setPos(-3.0, 24 - size, -5.0)
        self.leg4 = Cube(0, 16)
        self.leg4.addBox(-2.0, 0.0, -2.0, 4, size, 4, 0.0)
        self.leg4.setPos(3.0, 24 - size, -5.0)

    def render(self, x, y, z, xRot, yRot, zRot):
        self.head.yRot = xRot / 57.295776
        self.head.xRot = yRot / 57.295776
        self.body.xRot = math.pi / 2
        self.leg1.xRot = math.cos(x * 0.6662) * 1.4 * y
        self.leg2.xRot = math.cos(x * 0.6662 + math.pi) * 1.4 * y
        self.leg3.xRot = math.cos(x * 0.6662 + math.pi) * 1.4 * y
        self.leg4.xRot = math.cos(x * 0.6662) * 1.4 * y
        self.head.render(zRot)
        self.body.render(zRot)
        self.leg1.render(zRot)
        self.leg2.render(zRot)
        self.leg3.render(zRot)
        self.leg4.render(zRot)
