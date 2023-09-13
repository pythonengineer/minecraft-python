from mc.net.minecraft.model.QuadrupedModel import QuadrupedModel
from mc.net.minecraft.model.Cube import Cube

class SheepFurModel(QuadrupedModel):

    def __init__(self):
        super().__init__(12, 0.0)
        self.head = Cube(0, 0)
        self.head.addBox(-3.0, -4.0, -4.0, 6, 6, 6, 0.6)
        self.head.setPos(0.0, 6.0, -8.0)
        self.body = Cube(28, 8)
        self.body.addBox(-4.0, -10.0, -7.0, 8, 16, 6, 1.75)
        self.body.setPos(0.0, 5.0, 2.0)
        self.leg1 = Cube(0, 16)
        self.leg1.addBox(-2.0, 0.0, -2.0, 4, 6, 4, 0.5)
        self.leg1.setPos(-3.0, 12.0, 7.0)
        self.leg2 = Cube(0, 16)
        self.leg2.addBox(-2.0, 0.0, -2.0, 4, 6, 4, 0.5)
        self.leg2.setPos(3.0, 12.0, 7.0)
        self.leg3 = Cube(0, 16)
        self.leg3.addBox(-2.0, 0.0, -2.0, 4, 6, 4, 0.5)
        self.leg3.setPos(-3.0, 12.0, -5.0)
        self.leg4 = Cube(0, 16)
        self.leg4.addBox(-2.0, 0.0, -2.0, 4, 6, 4, 0.5)
        self.leg4.setPos(3.0, 12.0, -5.0)
