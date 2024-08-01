from mc.net.minecraft.client.model.ModelBiped import ModelBiped

import math

class ModelZombie(ModelBiped):

    def setRotationAngles(self, x, y, z, xRot, yRot, zRot):
        super().setRotationAngles(x, y, z, xRot, yRot, zRot)
        x = math.sin(0.0)
        y = math.sin(0.0)
        self.bipedRightArm.rotateAngleZ = 0.0
        self.bipedLeftArm.rotateAngleZ = 0.0
        self.bipedRightArm.rotateAngleY = -(0.1 - x * 0.6)
        self.bipedLeftArm.rotateAngleY = 0.1 - x * 0.6
        self.bipedRightArm.rotateAngleX = math.pi * -0.5
        self.bipedLeftArm.rotateAngleX = math.pi * -0.5
        self.bipedRightArm.rotateAngleX -= x * 1.2 - y * 0.4
        self.bipedLeftArm.rotateAngleX -= x * 1.2 - y * 0.4
        self.bipedRightArm.rotateAngleZ += math.cos(z * 0.09) * 0.05 + 0.05
        self.bipedLeftArm.rotateAngleZ -= math.cos(z * 0.09) * 0.05 + 0.05
        self.bipedRightArm.rotateAngleX += math.sin(z * 0.067) * 0.05
        self.bipedLeftArm.rotateAngleX -= math.sin(z * 0.067) * 0.05
