from mc.net.minecraft.character.Cube import Cube

class ZombieModel:

    def __init__(self):
        self.head = Cube(0, 0)
        self.head.addBox(-4.0, -8.0, -4.0, 8, 8, 8)

        self.body = Cube(16, 16)
        self.body.addBox(-4.0, 0.0, -2.0, 8, 12, 4)

        self.arm0 = Cube(40, 16)
        self.arm0.addBox(-3.0, -2.0, -2.0, 4, 12, 4)
        self.arm0.setPos(-5.0, 2.0, 0.0)

        self.arm1 = Cube(40, 16)
        self.arm1.addBox(-1.0, -2.0, -2.0, 4, 12, 4)
        self.arm1.setPos(5.0, 2.0, 0.0)

        self.leg0 = Cube(0, 16)
        self.leg0.addBox(-2.0, 0.0, -2.0, 4, 12, 4)
        self.leg0.setPos(-2.0, 12.0, 0.0)

        self.leg1 = Cube(0, 16)
        self.leg1.addBox(-2.0, 0.0, -2.0, 4, 12, 4)
        self.leg1.setPos(2.0, 12.0, 0.0)
