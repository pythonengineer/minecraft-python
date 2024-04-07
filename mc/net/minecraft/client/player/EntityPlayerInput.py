from mc.net.minecraft.game.entity.AILiving import AILiving

class EntityPlayerInput(AILiving):

    def __init__(self, player):
        super().__init__()
        self.__player = player

    def updatePlayerActionState(self):
        self._moveStrafing = self.__player.playerKeys.moveStrafe
        self._moveForward = self.__player.playerKeys.moveForward
        self._isJumping = self.__player.playerKeys.jump
