from mc.net.minecraft.character.Cube import Cube

import math

class ZombieModel:

    def __init__(self):
        self.head = Cube(0, 0)
        self.head.addBox(-4.0, -8.0, -4.0, 8, 8, 8)

        self.body = Cube(16, 16)
        self.body.addBox(-4.0, 0.0, -2.0, 8, 12, 4)

        self.arm0 = Cube(40, 16)
        self.arm0.addBox(-3.0, -2.0, -2.0, 4, 12, 4)
        self.arm0.setPos(-5.0, 2.0, 0.0)

        self.arm1 = Cube(40, 16)
        self.arm1.addBox(-1.0, -2.0, -2.0, 4, 12, 4)
        self.arm1.setPos(5.0, 2.0, 0.0)

        self.leg0 = Cube(0, 16)
        self.leg0.addBox(-2.0, 0.0, -2.0, 4, 12, 4)
        self.leg0.setPos(-2.0, 12.0, 0.0)

        self.leg1 = Cube(0, 16)
        self.leg1.addBox(-2.0, 0.0, -2.0, 4, 12, 4)
        self.leg1.setPos(2.0, 12.0, 0.0)

    def render(self, time):
        self.head.yRot = math.sin(time * 0.83) * 1.0
        self.head.xRot = math.sin(time) * 0.8

        self.arm0.xRot = math.sin(time * 0.6662 + math.pi) * 2.0
        self.arm0.zRot = (math.sin(time * 0.2312) + 1.0) * 1.0

        self.arm1.xRot = math.sin(time * 0.6662) * 2.0
        self.arm1.zRot = (math.sin(time * 0.2812) - 1.0) * 1.0

        self.leg0.xRot = math.sin(time * 0.6662) * 1.4
        self.leg1.xRot = math.sin(time * 0.6662 + math.pi) * 1.4

        self.head.render()
        self.body.render()
        self.arm0.render()
        self.arm1.render()
        self.leg0.render()
        self.leg1.render()
