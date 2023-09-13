from mc.net.minecraft.model.QuadrupedModel import QuadrupedModel
from mc.net.minecraft.model.Cube import Cube

class SheepModel(QuadrupedModel):

    def __init__(self):
        super().__init__(12, 0.0)
        self.head = Cube(0, 0)
        self.head.addBox(-3.0, -4.0, -6.0, 6, 6, 8, 0.8)
        self.head.setPos(0.0, 6.0, -8.0)
        self.body = Cube(28, 8)
        self.body.addBox(-4.0, -10.0, -7.0, 8, 16, 6, 0.0)
        self.body.setPos(0.0, 5.0, 2.0)
