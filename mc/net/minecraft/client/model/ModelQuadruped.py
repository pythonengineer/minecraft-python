from mc.net.minecraft.client.model.ModelRenderer import ModelRenderer
from mc.net.minecraft.client.model.ModelBase import ModelBase

import math

class ModelQuadruped(ModelBase):

    def __init__(self, yRot, _):
        self.bipedHead = ModelRenderer(0, 0)
        self.bipedHead.addBox(-4.0, -4.0, -8.0, 8, 8, 8, 0.0)
        self.bipedHead.setRotationPoint(0.0, 18 - yRot, -6.0)
        self.bipedBody = ModelRenderer(28, 8)
        self.bipedBody.addBox(-5.0, -10.0, -7.0, 10, 16, 8, 0.0)
        self.bipedBody.setRotationPoint(0.0, 17 - yRot, 2.0)
        self.__bipedRightLegFront = ModelRenderer(0, 16)
        self.__bipedRightLegFront.addBox(-2.0, 0.0, -2.0, 4, yRot, 4, 0.0)
        self.__bipedRightLegFront.setRotationPoint(-3.0, 24 - yRot, 7.0)
        self.__bipedLeftLegFront = ModelRenderer(0, 16)
        self.__bipedLeftLegFront.addBox(-2.0, 0.0, -2.0, 4, yRot, 4, 0.0)
        self.__bipedLeftLegFront.setRotationPoint(3.0, 24 - yRot, 7.0)
        self.__bipedRightLegBack = ModelRenderer(0, 16)
        self.__bipedRightLegBack.addBox(-2.0, 0.0, -2.0, 4, yRot, 4, 0.0)
        self.__bipedRightLegBack.setRotationPoint(-3.0, 24 - yRot, -5.0)
        self.__bipedLeftLegBack = ModelRenderer(0, 16)
        self.__bipedLeftLegBack.addBox(-2.0, 0.0, -2.0, 4, yRot, 4, 0.0)
        self.__bipedLeftLegBack.setRotationPoint(3.0, 24 - yRot, -5.0)

    def render(self, x, y, z, xRot, yRot, zRot):
        self.setRotationAngles(x, y, 0.0, xRot, yRot, 1.0)
        self.bipedHead.render(1.0)
        self.bipedBody.render(1.0)
        self.__bipedRightLegFront.render(1.0)
        self.__bipedLeftLegFront.render(1.0)
        self.__bipedRightLegBack.render(1.0)
        self.__bipedLeftLegBack.render(1.0)

    def setRotationAngles(self, x, y, z, xRot, yRot, zRot):
        self.bipedHead.rotateAngleY = xRot / (180.0 / math.pi)
        self.bipedHead.rotateAngleX = yRot / (180.0 / math.pi)
        self.bipedBody.rotateAngleX = math.pi * 0.5
        self.__bipedRightLegFront.rotateAngleX = math.cos(x * 0.6662) * 1.4 * y
        self.__bipedLeftLegFront.rotateAngleX = math.cos(x * 0.6662 + math.pi) * 1.4 * y
        self.__bipedRightLegBack.rotateAngleX = math.cos(x * 0.6662 + math.pi) * 1.4 * y
        self.__bipedLeftLegBack.rotateAngleX = math.cos(x * 0.6662) * 1.4 * y
