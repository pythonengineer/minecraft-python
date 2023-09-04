from mc.net.minecraft.mob.Zombie import Zombie
from mc.net.minecraft.model.SkeletonModel import SkeletonModel

class Skeleton(Zombie):
    __skeletonModel = SkeletonModel()

    def __init__(self, level, x, y, z):
        super().__init__(level, x, y, z)
        self.model = self._humanoidModel = Skeleton.__skeletonModel
        self._textureName = 'mob/skeleton.png'
