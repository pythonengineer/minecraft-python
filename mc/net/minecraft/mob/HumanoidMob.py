from mc.net.minecraft.mob.Mob import Mob
from mc.net.minecraft.model.HumanoidModel import HumanoidModel
from pyglet import gl

import random

class HumanoidMob(Mob):
    __model1 = HumanoidModel(0.0)
    __model2 = HumanoidModel(1.0)

    def __init__(self, level, x, y, z):
        super().__init__(level)
        self._humanoidModel = HumanoidMob.__model1
        self.__helmet = random.random() < 0.2
        self.__body = random.random() < 0.2
        self.setPos(x, y, z)

    def renderModel(self, textures, x, y, z, rotX, rotY, rotZ):
        self.model.render(x, z, self._tickCount + y, rotX, rotY, rotZ)
        gl.glEnable(gl.GL_ALPHA_TEST)
        if self.allowAlpha:
            gl.glEnable(gl.GL_CULL_FACE)
        if self.hasHair:
            gl.glDisable(gl.GL_CULL_FACE)
            self._humanoidModel.hair.yRot = self._humanoidModel.head.yRot
            self._humanoidModel.hair.xRot = self._humanoidModel.head.xRot
            self._humanoidModel.hair.render(rotZ)
            gl.glEnable(gl.GL_CULL_FACE)
        if self.__body or self.__helmet:
            gl.glBindTexture(gl.GL_TEXTURE_2D, textures.loadTexture('armor/plate.png'))
            gl.glDisable(gl.GL_CULL_FACE)
            self.__model2.head.showModel = self.__helmet
            self.__model2.body.showModel = self.__body
            self.__model2.rightArm.showModel = self.__body
            self.__model2.leftArm.showModel = self.__body
            self.__model2.rightLeg.showModel = False
            self.__model2.leftLeg.showModel = False
            self.__model2.head.yRot = self._humanoidModel.head.yRot
            self.__model2.head.xRot = self._humanoidModel.head.xRot
            self.__model2.rightArm.xRot = self._humanoidModel.rightArm.xRot
            self.__model2.rightArm.zRot = self._humanoidModel.rightArm.zRot
            self.__model2.leftArm.xRot = self._humanoidModel.leftArm.xRot
            self.__model2.leftArm.zRot = self._humanoidModel.leftArm.zRot
            self.__model2.rightLeg.xRot = self._humanoidModel.rightLeg.xRot
            self.__model2.leftLeg.xRot = self._humanoidModel.leftLeg.xRot
            self.__model2.head.render(rotZ)
            self.__model2.body.render(rotZ)
            self.__model2.rightArm.render(rotZ)
            self.__model2.leftArm.render(rotZ)
            self.__model2.rightLeg.render(rotZ)
            self.__model2.leftLeg.render(rotZ)
            gl.glEnable(gl.GL_CULL_FACE)

        gl.glDisable(gl.GL_ALPHA_TEST)
