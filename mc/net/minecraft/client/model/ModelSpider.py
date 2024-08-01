from mc.net.minecraft.client.model.ModelRenderer import ModelRenderer
from mc.net.minecraft.client.model.ModelBase import ModelBase

import math

class ModelSpider(ModelBase):

    def __init__(self):
        self.__spiderHead = ModelRenderer(32, 4)
        self.__spiderHead.addBox(-4.0, -4.0, -8.0, 8, 8, 8, 0.0)
        self.__spiderHead.setRotationPoint(0.0, 14.0, -3.0)
        self.__spiderNeck = ModelRenderer(0, 0)
        self.__spiderNeck.addBox(-3.0, -3.0, -3.0, 6, 6, 6, 0.0)
        self.__spiderNeck.setRotationPoint(0.0, 14.0, 0.0)
        self.__spiderBody = ModelRenderer(0, 12)
        self.__spiderBody.addBox(-5.0, -4.0, -6.0, 10, 8, 12, 0.0)
        self.__spiderBody.setRotationPoint(0.0, 14.0, 9.0)
        self.__spiderLeg1 = ModelRenderer(18, 0)
        self.__spiderLeg1.addBox(-15.0, -1.0, -1.0, 16, 2, 2, 0.0)
        self.__spiderLeg1.setRotationPoint(-4.0, 14.0, 2.0)
        self.__spiderLeg2 = ModelRenderer(18, 0)
        self.__spiderLeg2.addBox(-1.0, -1.0, -1.0, 16, 2, 2, 0.0)
        self.__spiderLeg2.setRotationPoint(4.0, 14.0, 2.0)
        self.__spiderLeg3 = ModelRenderer(18, 0)
        self.__spiderLeg3.addBox(-15.0, -1.0, -1.0, 16, 2, 2, 0.0)
        self.__spiderLeg3.setRotationPoint(-4.0, 14.0, 1.0)
        self.__spiderLeg4 = ModelRenderer(18, 0)
        self.__spiderLeg4.addBox(-1.0, -1.0, -1.0, 16, 2, 2, 0.0)
        self.__spiderLeg4.setRotationPoint(4.0, 14.0, 1.0)
        self.__spiderLeg5 = ModelRenderer(18, 0)
        self.__spiderLeg5.addBox(-15.0, -1.0, -1.0, 16, 2, 2, 0.0)
        self.__spiderLeg5.setRotationPoint(-4.0, 14.0, 0.0)
        self.__spiderLeg6 = ModelRenderer(18, 0)
        self.__spiderLeg6.addBox(-1.0, -1.0, -1.0, 16, 2, 2, 0.0)
        self.__spiderLeg6.setRotationPoint(4.0, 14.0, 0.0)
        self.__spiderLeg7 = ModelRenderer(18, 0)
        self.__spiderLeg7.addBox(-15.0, -1.0, -1.0, 16, 2, 2, 0.0)
        self.__spiderLeg7.setRotationPoint(-4.0, 14.0, -1.0)
        self.__spiderLeg8 = ModelRenderer(18, 0)
        self.__spiderLeg8.addBox(-1.0, -1.0, -1.0, 16, 2, 2, 0.0)
        self.__spiderLeg8.setRotationPoint(4.0, 14.0, -1.0)

    def render(self, x, y, z, xRot, yRot, zRot):
        self.setRotationAngles(x, y, 0.0, xRot, yRot, 1.0)
        self.__spiderHead.render(1.0)
        self.__spiderNeck.render(1.0)
        self.__spiderBody.render(1.0)
        self.__spiderLeg1.render(1.0)
        self.__spiderLeg2.render(1.0)
        self.__spiderLeg3.render(1.0)
        self.__spiderLeg4.render(1.0)
        self.__spiderLeg5.render(1.0)
        self.__spiderLeg6.render(1.0)
        self.__spiderLeg7.render(1.0)
        self.__spiderLeg8.render(1.0)

    def setRotationAngles(self, x, y, z, xRot, yRot, zRot):
        self.__spiderHead.rotateAngleY = xRot / (180.0 / math.pi)
        self.__spiderHead.rotateAngleX = yRot / (180.0 / math.pi)
        self.__spiderLeg1.rotateAngleZ = math.pi * -0.25
        self.__spiderLeg2.rotateAngleZ = math.pi * 0.25
        self.__spiderLeg3.rotateAngleZ = -math.pi * 0.185
        self.__spiderLeg4.rotateAngleZ = math.pi * 0.185
        self.__spiderLeg5.rotateAngleZ = -math.pi * 0.185
        self.__spiderLeg6.rotateAngleZ = math.pi * 0.185
        self.__spiderLeg7.rotateAngleZ = math.pi * -0.25
        self.__spiderLeg8.rotateAngleZ = math.pi * 0.25
        self.__spiderLeg1.rotateAngleY = math.pi * 0.25
        self.__spiderLeg2.rotateAngleY = math.pi * -0.25
        self.__spiderLeg3.rotateAngleY = math.pi * 0.125
        self.__spiderLeg4.rotateAngleY = math.pi * -0.125
        self.__spiderLeg5.rotateAngleY = math.pi * -0.125
        self.__spiderLeg6.rotateAngleY = math.pi * 0.125
        self.__spiderLeg7.rotateAngleY = math.pi * -0.25
        self.__spiderLeg8.rotateAngleY = math.pi * 0.25
        rotY0 = -(math.cos(x * 0.6662 * 2.0) * 0.4) * y
        rotY1 = -(math.cos(x * 0.6662 * 2.0 + math.pi) * 0.4) * y
        rotY2 = -(math.cos(x * 0.6662 * 2.0 + math.pi * 0.5) * 0.4) * y
        rotY3 = -(math.cos(x * 0.6662 * 2.0 + math.pi * 3.0 / 2.0) * 0.4) * y
        rotZ0 = abs(math.sin(x * 0.6662) * 0.4) * y
        rotZ1 = abs(math.sin(x * 0.6662 + math.pi) * 0.4) * y
        rotZ2 = abs(math.sin(x * 0.6662 + math.pi * 0.5) * 0.4) * y
        rotZ3 = abs(math.sin(x * 0.6662 + math.pi * 3.0 / 2.0) * 0.4) * y
        self.__spiderLeg1.rotateAngleY += rotY0
        self.__spiderLeg2.rotateAngleY -= rotY0
        self.__spiderLeg3.rotateAngleY += rotY1
        self.__spiderLeg4.rotateAngleY -= rotY1
        self.__spiderLeg5.rotateAngleY += rotY2
        self.__spiderLeg6.rotateAngleY -= rotY2
        self.__spiderLeg7.rotateAngleY += rotY3
        self.__spiderLeg8.rotateAngleY -= rotY3
        self.__spiderLeg1.rotateAngleZ += rotZ0
        self.__spiderLeg2.rotateAngleZ -= rotZ0
        self.__spiderLeg3.rotateAngleZ += rotZ1
        self.__spiderLeg4.rotateAngleZ -= rotZ1
        self.__spiderLeg5.rotateAngleZ += rotZ2
        self.__spiderLeg6.rotateAngleZ -= rotZ2
        self.__spiderLeg7.rotateAngleZ += rotZ3
        self.__spiderLeg8.rotateAngleZ -= rotZ3
