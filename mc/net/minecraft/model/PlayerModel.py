from mc.net.minecraft.model.HumanoidModel import HumanoidModel

class PlayerModel(HumanoidModel):

    def __init__(self, translation=0.0):
        super().__init__(translation)
        self.head.isHidden = True
