from mc.net.minecraft.client.model.ModelBase import ModelBase
from mc.net.minecraft.client.model.ModelRenderer import ModelRenderer

class ModelBiped(ModelBase):

    def __init__(self, translation=0.0):
        self.bipedHead = ModelRenderer(0, 0)
        self.bipedHead.setBounds(-4.0, -8.0, -4.0, 8, 8, 8, 0.0)
        self.bipedHeadWear = ModelRenderer(32, 0)
        self.bipedHeadWear.setBounds(-4.0, -8.0, -4.0, 8, 8, 8, 0.5)
        self.bipedBody = ModelRenderer(16, 16)
        self.bipedBody.setBounds(-4.0, 0.0, -2.0, 8, 12, 4, 0.0)
        self.bipedRightArm = ModelRenderer(40, 16)
        self.bipedRightArm.setBounds(-3.0, -2.0, -2.0, 4, 12, 4, 0.0)
        self.bipedLeftArm = ModelRenderer(40, 16)
        self.bipedLeftArm.mirror = True
        self.bipedLeftArm.setBounds(-1.0, -2.0, -2.0, 4, 12, 4, 0.0)
        self.bipedRightLeg = ModelRenderer(0, 16)
        self.bipedRightLeg.setBounds(-2.0, 0.0, -2.0, 4, 12, 4, 0.0)
        self.bipedLeftLeg = ModelRenderer(0, 16)
        self.bipedLeftLeg.mirror = True
        self.bipedLeftLeg.setBounds(-2.0, 0.0, -2.0, 4, 12, 4, 0.0)
