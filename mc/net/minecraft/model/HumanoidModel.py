from mc.net.minecraft.model.BaseModel import BaseModel
from mc.net.minecraft.model.Cube import Cube

import math

class HumanoidModel(BaseModel):

    def __init__(self, translation=0.0):
        self.head = Cube(0, 0)
        self.head.addBox(-4.0, -8.0, -4.0, 8, 8, 8, translation)
        self.hair = Cube(32, 0)
        self.hair.addBox(-4.0, -8.0, -4.0, 8, 8, 8, translation + 0.5)
        self.body = Cube(16, 16)
        self.body.addBox(-4.0, 0.0, -2.0, 8, 12, 4, translation)
        self.rightArm = Cube(40, 16)
        self.rightArm.addBox(-3.0, -2.0, -2.0, 4, 12, 4, translation)
        self.rightArm.setPos(-5.0, 2.0, 0.0)
        self.leftArm = Cube(40, 16)
        self.leftArm.mirror = True
        self.leftArm.addBox(-1.0, -2.0, -2.0, 4, 12, 4, translation)
        self.leftArm.setPos(5.0, 2.0, 0.0)
        self.rightLeg = Cube(0, 16)
        self.rightLeg.addBox(-2.0, 0.0, -2.0, 4, 12, 4, translation)
        self.rightLeg.setPos(-2.0, 12.0, 0.0)
        self.leftLeg = Cube(0, 16)
        self.leftLeg.mirror = True
        self.leftLeg.addBox(-2.0, 0.0, -2.0, 4, 12, 4, translation)
        self.leftLeg.setPos(2.0, 12.0, 0.0)

    def render(self, x, y, z, xRot, yRot, zRot):
        self.setupAnim(x, y, z, xRot, yRot, zRot)
        self.head.render(zRot)
        self.body.render(zRot)
        self.rightArm.render(zRot)
        self.leftArm.render(zRot)
        self.rightLeg.render(zRot)
        self.leftLeg.render(zRot)

    def setupAnim(self, x, y, xRot, yRot, zRot, translation):
        self.head.yRot = yRot / 57.295776
        self.head.xRot = zRot / 57.295776
        self.rightArm.xRot = math.cos(x * 0.6662 + math.pi) * 2.0 * y
        self.rightArm.zRot = (math.cos(x * 0.2312) + 1.0) * y
        self.leftArm.xRot = math.cos(x * 0.6662) * 2.0 * y
        self.leftArm.zRot = (math.cos(x * 0.2812) - 1.0) * y
        self.rightLeg.xRot = math.cos(x * 0.6662) * 1.4 * y
        self.leftLeg.xRot = math.cos(x * 0.6662 + math.pi) * 1.4 * y
        self.rightArm.zRot += math.cos(xRot * 0.09) * 0.05 + 0.05
        self.leftArm.zRot -= math.cos(xRot * 0.09) * 0.05 + 0.05
        self.rightArm.xRot += math.sin(xRot * 0.067) * 0.05
        self.leftArm.xRot -= math.sin(xRot * 0.067) * 0.05
