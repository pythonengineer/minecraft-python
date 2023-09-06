from mc.net.minecraft.model.Cube import Cube
from mc.net.minecraft.model.ZombieModel import ZombieModel

class SkeletonModel(ZombieModel):

    def __init__(self):
        super().__init__()
        self.rightArm = Cube(40, 16)
        self.rightArm.addBox(-1.0, -2.0, -1.0, 2, 12, 2, 0.0)
        self.rightArm.setPos(-5.0, 2.0, 0.0)
        self.leftArm = Cube(40, 16)
        self.leftArm.mirror = True
        self.leftArm.addBox(-1.0, -2.0, -1.0, 2, 12, 2, 0.0)
        self.leftArm.setPos(5.0, 2.0, 0.0)
        self.rightLeg = Cube(0, 16)
        self.rightLeg.addBox(-1.0, 0.0, -1.0, 2, 12, 2, 0.0)
        self.rightLeg.setPos(-2.0, 12.0, 0.0)
        self.leftLeg = Cube(0, 16)
        self.leftLeg.mirror = True
        self.leftLeg.addBox(-1.0, 0.0, -1.0, 2, 12, 2, 0.0)
        self.leftLeg.setPos(2.0, 12.0, 0.0)
