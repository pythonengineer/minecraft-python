from mc.net.minecraft.model.Cube import Cube

class SignModel:

    def __init__(self):
        self.signBoard = Cube(0, 0)
        self.signBoard.addBox(-12.0, -14.0, -1.0, 24, 12, 2, 0.0)
        self.signStick = Cube(0, 14)
        self.signStick.addBox(-1.0, -2.0, -1.0, 2, 14, 2, 0.0)
