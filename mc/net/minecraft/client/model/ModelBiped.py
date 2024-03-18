from mc.net.minecraft.client.model.ModelBase import ModelBase
from mc.net.minecraft.client.model.ModelRenderer import ModelRenderer

class ModelBiped(ModelBase):

    def __init__(self, translation=0.0):
        self.bipedHead = ModelRenderer(0, 0)
        self.bipedHead.addBox(-4.0, -8.0, -4.0, 8, 8, 8, 0.0)
        self.bipedHeadWear = ModelRenderer(32, 0)
        self.bipedHeadWear.addBox(-4.0, -8.0, -4.0, 8, 8, 8, 0.0 + 0.5)
        self.bipedBody = ModelRenderer(16, 16)
        self.bipedBody.addBox(-4.0, 0.0, -2.0, 8, 12, 4, 0.0)
        self.bipedRightArm = ModelRenderer(40, 16)
        self.bipedRightArm.addBox(-3.0, -2.0, -2.0, 4, 12, 4, 0.0)
        self.bipedLeftArm2 = ModelRenderer(40, 16)
        self.bipedLeftArm2.mirror = True
        self.bipedLeftArm2.addBox(-1.0, -2.0, -2.0, 4, 12, 4, 0.0)
        self.bipedRightLeg = ModelRenderer(0, 16)
        self.bipedRightLeg.addBox(-2.0, 0.0, -2.0, 4, 12, 4, 0.0)
        self.bipedLeftLeg = ModelRenderer(0, 16)
        self.bipedLeftLeg.mirror = True
        self.bipedLeftLeg.addBox(-2.0, 0.0, -2.0, 4, 12, 4, 0.0)
