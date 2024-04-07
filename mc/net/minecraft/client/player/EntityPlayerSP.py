from mc.net.minecraft.client.player.EntityPlayerInput import EntityPlayerInput
from mc.net.minecraft.game.entity.player.EntityPlayer import EntityPlayer

class EntityPlayerSP(EntityPlayer):

    def __init__(self, world):
        super().__init__(world)
        self.playerKeys = None
        self._entityAI = EntityPlayerInput(self)

    def onLivingUpdate(self):
        self.playerKeys.updatePlayerMoveState()
        super().onLivingUpdate()
