from mc.net.minecraft.mob.ai.BasicAttackAI import BasicAttackAI

class JumpAttackAI(BasicAttackAI):

    def __init__(self):
        super().__init__()
        self.runSpeed *= 8.0

    def _jumpFromGround(self):
        if not self.attackTarget:
            super()._jumpFromGround()
        else:
            self.mob.xd = 0.0
            self.mob.zd = 0.0
            self.mob.moveRelative(0.0, 1.0, 0.6)
            self.mob.yd = 0.5
