from mc.net.minecraft.mob.ai.BasicAI import BasicAI

class PlayerInput(BasicAI):

    def __init__(self, player):
        super().__init__()
        self.__player = player

    def update(self):
        self.jumping = self.__player.input.jumping
        self.xxa = self.__player.input.ya
        self.yya = self.__player.input.xa
