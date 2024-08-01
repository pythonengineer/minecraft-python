from mc.net.minecraft.client.model.ModelRenderer import ModelRenderer
from mc.net.minecraft.client.model.ModelZombie import ModelZombie

class ModelSkeleton(ModelZombie):

    def __init__(self):
        super().__init__()
        self.bipedRightArm = ModelRenderer(40, 16)
        self.bipedRightArm.addBox(-1.0, -2.0, -1.0, 2, 12, 2, 0.0)
        self.bipedRightArm.setRotationPoint(-5.0, 2.0, 0.0)
        self.bipedLeftArm = ModelRenderer(40, 16)
        self.bipedLeftArm.mirror = True
        self.bipedLeftArm.addBox(-1.0, -2.0, -1.0, 2, 12, 2, 0.0)
        self.bipedLeftArm.setRotationPoint(5.0, 2.0, 0.0)
        self.bipedRightLeg = ModelRenderer(0, 16)
        self.bipedRightLeg.addBox(-1.0, 0.0, -1.0, 2, 12, 2, 0.0)
        self.bipedRightLeg.setRotationPoint(-2.0, 12.0, 0.0)
        self.bipedLeftLeg = ModelRenderer(0, 16)
        self.bipedLeftLeg.mirror = True
        self.bipedLeftLeg.addBox(-1.0, 0.0, -1.0, 2, 12, 2, 0.0)
        self.bipedLeftLeg.setRotationPoint(2.0, 12.0, 0.0)
