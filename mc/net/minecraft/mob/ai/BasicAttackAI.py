from mc.net.minecraft.mob.ai.BasicAI import BasicAI

class BasicAttackAI(BasicAI):

    def _tick(self):
        super()._tick()
        self._attack(self.level.getPlayer())
