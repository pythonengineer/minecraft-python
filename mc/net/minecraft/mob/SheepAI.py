from mc.net.minecraft.mob.ai.BasicAI import BasicAI
from mc.net.minecraft.level.tile.Tiles import tiles

import random
import math

class SheepAI(BasicAI):

    def update(self):
        rotX = -0.7 * math.sin(self.mob.yRot * math.pi / 180.0)
        rotY = 0.7 * math.cos(self.mob.yRot * math.pi / 180.0)
        x = int(self.mob.x + rotX)
        y = int(self.mob.y - 2.0)
        z = int(self.mob.z + rotY)
        if self.mob.grazing:
            if self.level.getTile(x, y, z) != tiles.grass.id:
                self.mob.grazing = False
            else:
                self.mob.grazingTime += 1
                if self.mob.grazingTime == 60:
                    self.level.setTile(x, y, z, tiles.dirt.id)
                    if math.floor(random.random() * 5) == 0:
                        self.mob.hasFur = True

                self.xxa = 0.0
                self.yya = 0.0
                self.mob.xRot = 40 + self.mob.grazingTime / 2 % 2 * 10
        else:
            if self.level.getTile(x, y, z) == tiles.grass.id:
                self.mob.grazing = True
                self.mob.grazingTime = 0

            super().update()
