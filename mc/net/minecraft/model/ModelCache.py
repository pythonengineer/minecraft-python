from mc.net.minecraft.model.HumanoidModel import HumanoidModel
from mc.net.minecraft.model.CreeperModel import CreeperModel
from mc.net.minecraft.model.SkeletonModel import SkeletonModel
from mc.net.minecraft.model.ZombieModel import ZombieModel
from mc.net.minecraft.model.QuadrupedModel import QuadrupedModel

class ModelCache:

    def __init__(self):
        self.__humanoidModel = HumanoidModel(0.0)
        self.__humanoidArmorModel = HumanoidModel(1.0)
        self.__creeperModel = CreeperModel()
        self.__skeletonModel = SkeletonModel()
        self.__zombieModel = ZombieModel()
        self.__quadrupedModel = QuadrupedModel()

    def getModel(self, name):
        if name == 'humanoid':
            return self.__humanoidModel
        elif name == 'humanoid.armor':
            return self.__humanoidArmorModel
        elif name == 'creeper':
            return self.__creeperModel
        elif name == 'skeleton':
            return self.__skeletonModel
        elif name == 'zombie':
            return self.__zombieModel
        elif name == 'pig':
            return self.__quadrupedModel