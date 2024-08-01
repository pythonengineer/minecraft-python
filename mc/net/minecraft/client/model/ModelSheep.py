from mc.net.minecraft.client.model.ModelQuadruped import ModelQuadruped
from mc.net.minecraft.client.model.ModelRenderer import ModelRenderer

class ModelSheep(ModelQuadruped):

    def __init__(self):
        super().__init__(12, 0.0)
        self.bipedHead = ModelRenderer(0, 0)
        self.bipedHead.addBox(-3.0, -4.0, -6.0, 6, 6, 8, 0.0)
        self.bipedHead.setRotationPoint(0.0, 6.0, -8.0)
        self.bipedBody = ModelRenderer(28, 8)
        self.bipedBody.addBox(-4.0, -10.0, -7.0, 8, 16, 6, 0.0)
        self.bipedBody.setRotationPoint(0.0, 5.0, 2.0)
