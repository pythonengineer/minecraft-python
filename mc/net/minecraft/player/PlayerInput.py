from mc.net.minecraft.mob.ai.BasicAI import BasicAI

class PlayerInput(BasicAI):

    def __init__(self, player, keyboardInput):
        super().__init__()
        self.__input = keyboardInput

    def _tick(self):
        self.jumping = self.__input.jumping
        self.xxa = self.__input.ya
        self.yya = self.__input.xa
