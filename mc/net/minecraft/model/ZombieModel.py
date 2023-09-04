from mc.net.minecraft.model.HumanoidModel import HumanoidModel

import math

class ZombieModel(HumanoidModel):

    def setupAnim(self, x, y, xRot, yRot, zRot, translation):
        super().setupAnim(x, y, xRot, yRot, zRot, translation)
        x = math.sin(self.rot * math.pi)
        y = math.sin((1.0 - (1.0 - self.rot) * (1.0 - self.rot)) * math.pi)
        self.rightArm.zRot = 0.0
        self.leftArm.zRot = 0.0
        self.rightArm.yRot = -(0.1 - x * 0.6)
        self.leftArm.yRot = 0.1 - x * 0.6
        self.rightArm.xRot = -1.5707964
        self.leftArm.xRot = -1.5707964
        self.rightArm.xRot -= x * 1.2 - y * 0.4
        self.leftArm.xRot -= x * 1.2 - y * 0.4
        self.rightArm.zRot += math.cos(xRot * 0.09) * 0.05 + 0.05
        self.leftArm.zRot -= math.cos(xRot * 0.09) * 0.05 + 0.05
        self.rightArm.xRot += math.sin(xRot * 0.067) * 0.05
        self.leftArm.xRot -= math.sin(xRot * 0.067) * 0.05
