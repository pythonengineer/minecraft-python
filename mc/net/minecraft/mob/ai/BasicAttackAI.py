from mc.net.minecraft.mob.ai.BasicAI import BasicAI
from mc.net.minecraft.item.Arrow import Arrow
from mc.net.minecraft.model.Vec3 import Vec3

import random
import math

class BasicAttackAI(BasicAI):

    def __init__(self):
        super().__init__()
        self.damage = 6

    def update(self):
        super().update()
        if self.mob.health > 0:
            self._doAttack()

    def _doAttack(self):
        entity = self.level.getPlayer()
        dd = 16.0
        if self.attackTarget and self.attackTarget.removed:
            self.attackTarget = None

        if entity and not self.attackTarget:
            xd = entity.x - self.mob.x
            yd = entity.y - self.mob.y
            zd = entity.z - self.mob.z
            if xd * xd + yd * yd + zd * zd < dd * dd:
                self.attackTarget = entity

        if self.attackTarget:
            xd = self.attackTarget.x - self.mob.x
            yd = self.attackTarget.y - self.mob.y
            zd = self.attackTarget.z - self.mob.z
            if xd * xd + yd * yd + zd * zd > dd * dd * 2.0 * 2.0 and random.randint(0, 100) == 0:
                self.attackTarget = None

            if self.attackTarget:
                f6 = math.sqrt(xd * xd + yd * yd + zd * zd)
                self.mob.yRot = (math.atan2(zd, xd) * 180.0 / math.pi) - 90.0
                self.mob.xRot = -((math.atan2(yd, f6) * 180.0 / math.pi))
                if math.sqrt(xd * xd + yd * yd + zd * zd) < 2.0 and self._attackDelay == 0:
                    self.attack(self.attackTarget)

    def attack(self, entity):
        if self.level.clip(Vec3(self.mob.x, self.mob.y, self.mob.z), Vec3(entity.x, entity.y, entity.z)):
            return False
        else:
            self.mob.attackTime = 5
            self._attackDelay = int(random.random() * 20) + 10
            hp = int((random.random() + random.random()) / 2.0 * self.damage + 1.0)
            entity.hurt(self.mob, hp)
            self._noActionTime = 0
            return True

    def hurt(self, entity, hp):
        super().hurt(entity, hp)
        if isinstance(entity, Arrow):
            entity = entity.getOwner()

        if entity and entity != self.mob:
            self.attackTarget = entity
