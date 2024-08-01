from mc.net.minecraft.client.model.ModelBase import ModelBase
from mc.net.minecraft.client.model.ModelRenderer import ModelRenderer

import math

class ModelBiped(ModelBase):

    def __init__(self, translation=0.0):
        self.bipedHead = ModelRenderer(0, 0)
        self.bipedHead.addBox(-4.0, -8.0, -4.0, 8, 8, 8, 0.0)
        self.bipedHeadWear = ModelRenderer(32, 0)
        self.bipedHeadWear.addBox(-4.0, -8.0, -4.0, 8, 8, 8, 0.5)
        self.bipedBody = ModelRenderer(16, 16)
        self.bipedBody.addBox(-4.0, 0.0, -2.0, 8, 12, 4, 0.0)
        self.bipedRightArm = ModelRenderer(40, 16)
        self.bipedRightArm.addBox(-3.0, -2.0, -2.0, 4, 12, 4, 0.0)
        self.bipedRightArm.setRotationPoint(-5.0, 2.0, 0.0)
        self.bipedLeftArm = ModelRenderer(40, 16)
        self.bipedLeftArm.mirror = True
        self.bipedLeftArm.addBox(-1.0, -2.0, -2.0, 4, 12, 4, 0.0)
        self.bipedLeftArm.setRotationPoint(5.0, 2.0, 0.0)
        self.bipedRightLeg = ModelRenderer(0, 16)
        self.bipedRightLeg.addBox(-2.0, 0.0, -2.0, 4, 12, 4, 0.0)
        self.bipedRightLeg.setRotationPoint(-2.0, 12.0, 0.0)
        self.bipedLeftLeg = ModelRenderer(0, 16)
        self.bipedLeftLeg.mirror = True
        self.bipedLeftLeg.addBox(-2.0, 0.0, -2.0, 4, 12, 4, 0.0)
        self.bipedLeftLeg.setRotationPoint(2.0, 12.0, 0.0)

    def render(self, x, y, z, xRot, yRot, zRot):
        self.setRotationAngles(x, y, 0.0, xRot, yRot, 1.0)
        self.bipedHead.render(1.0)
        self.bipedBody.render(1.0)
        self.bipedRightArm.render(1.0)
        self.bipedLeftArm.render(1.0)
        self.bipedRightLeg.render(1.0)
        self.bipedLeftLeg.render(1.0)

    def setRotationAngles(self, x, y, z, xRot, yRot, zRot):
        self.bipedHead.rotateAngleY = xRot / (180.0 / math.pi)
        self.bipedHead.rotateAngleX = yRot / (180.0 / math.pi)
        self.bipedRightArm.rotateAngleX = math.cos(x * 0.6662 + math.pi) * 2.0 * y
        self.bipedRightArm.rotateAngleZ = (math.cos(x * 0.2312) + 1.0) * y
        self.bipedLeftArm.rotateAngleX = math.cos(x * 0.6662) * 2.0 * y
        self.bipedLeftArm.rotateAngleZ = (math.cos(x * 0.2812) - 1.0) * y
        self.bipedRightLeg.rotateAngleX = math.cos(x * 0.6662) * 1.4 * y
        self.bipedLeftLeg.rotateAngleX = math.cos(x * 0.6662 + math.pi) * 1.4 * y
        self.bipedRightArm.rotateAngleZ += math.cos(z * 0.09) * 0.05 + 0.05
        self.bipedLeftArm.rotateAngleZ -= math.cos(z * 0.09) * 0.05 + 0.05
        self.bipedRightArm.rotateAngleX += math.sin(z * 0.067) * 0.05
        self.bipedLeftArm.rotateAngleX -= math.sin(z * 0.067) * 0.05
