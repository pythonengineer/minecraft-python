from mc.net.minecraft.game.entity.AILiving import AILiving

class EntityPlayerInput(AILiving):

    def __init__(self, player):
        super().__init__()
        self.__player = player

    def updatePlayerActionState(self):
        self.moveStrafing = self.__player.movementInput.moveStrafe
        self.moveForward = self.__player.movementInput.moveForward
        self.isJumping = self.__player.movementInput.jump
