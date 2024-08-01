from mc.net.minecraft.client.model.ModelRenderer import ModelRenderer
from mc.net.minecraft.client.model.ModelBase import ModelBase

import math

class ModelCreeper(ModelBase):

    def __init__(self):
        self.__creeperHead = ModelRenderer(0, 0)
        self.__creeperHead.addBox(-4.0, -8.0, -4.0, 8, 8, 8, 0.0)
        self.__creeperHead.setRotationPoint(0.0, 4.0, 0.0)
        self.__creeperHeadWear = ModelRenderer(32, 0)
        self.__creeperHeadWear.addBox(-4.0, -8.0, -4.0, 8, 8, 8, 0.5)
        self.__creeperHeadWear.setRotationPoint(0.0, 4.0, 0.0)
        self.__creeperBody = ModelRenderer(16, 16)
        self.__creeperBody.addBox(-4.0, 0.0, -2.0, 8, 12, 4, 0.0)
        self.__creeperBody.setRotationPoint(0.0, 4.0, 0.0)
        self.__creeperLeg1 = ModelRenderer(0, 16)
        self.__creeperLeg1.addBox(-2.0, 0.0, -2.0, 4, 6, 4, 0.0)
        self.__creeperLeg1.setRotationPoint(-2.0, 16.0, 4.0)
        self.__creeperLeg2 = ModelRenderer(0, 16)
        self.__creeperLeg2.addBox(-2.0, 0.0, -2.0, 4, 6, 4, 0.0)
        self.__creeperLeg2.setRotationPoint(2.0, 16.0, 4.0)
        self.__creeperLeg3 = ModelRenderer(0, 16)
        self.__creeperLeg3.addBox(-2.0, 0.0, -2.0, 4, 6, 4, 0.0)
        self.__creeperLeg3.setRotationPoint(-2.0, 16.0, -4.0)
        self.__creeperLeg4 = ModelRenderer(0, 16)
        self.__creeperLeg4.addBox(-2.0, 0.0, -2.0, 4, 6, 4, 0.0)
        self.__creeperLeg4.setRotationPoint(2.0, 16.0, -4.0)

    def render(self, x, y, z, xRot, yRot, zRot):
        self.setRotationAngles(x, y, 0.0, xRot, yRot, 1.0)
        self.__creeperHead.render(1.0)
        self.__creeperBody.render(1.0)
        self.__creeperLeg1.render(1.0)
        self.__creeperLeg2.render(1.0)
        self.__creeperLeg3.render(1.0)
        self.__creeperLeg4.render(1.0)

    def setRotationAngles(self, x, y, z, xRot, yRot, zRot):
        self.__creeperHead.rotateAngleY = yRot / (180.0 / math.pi)
        self.__creeperHead.rotateAngleX = xRot / (180.0 / math.pi)
        self.__creeperLeg1.rotateAngleX = math.cos(x * 0.6662) * 1.4 * y
        self.__creeperLeg2.rotateAngleX = math.cos(x * 0.6662 + math.pi) * 1.4 * y
        self.__creeperLeg3.rotateAngleX = math.cos(x * 0.6662 + math.pi) * 1.4 * y
        self.__creeperLeg4.rotateAngleX = math.cos(x * 0.6662) * 1.4 * y
