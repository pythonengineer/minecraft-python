from mc.net.minecraft.mob.Mob import Mob
from pyglet import gl

import random

class HumanoidMob(Mob):

    def __init__(self, level, x, y, z):
        super().__init__(level)
        self.__helmet = random.random() < 0.2
        self.__armor = random.random() < 0.2
        self.setPos(x, y, z)

    def renderModel(self, textures, x, y, z, rotX, rotY, rotZ):
        model = self.modelCache.getModel(self.modelName)
        model.render(x, z, self._tickCount + y, rotX, rotY, rotZ)
        gl.glEnable(gl.GL_ALPHA_TEST)
        if self.allowAlpha:
            gl.glEnable(gl.GL_CULL_FACE)
        if self.hasHair:
            gl.glDisable(gl.GL_CULL_FACE)
            model.hair.yRot = model.head.yRot
            model.hair.xRot = model.head.xRot
            model.hair.render(rotZ)
            gl.glEnable(gl.GL_CULL_FACE)
        if self.__armor or self.__helmet:
            gl.glBindTexture(gl.GL_TEXTURE_2D, textures.loadTexture('armor/plate.png'))
            gl.glDisable(gl.GL_CULL_FACE)
            model2 = self.modelCache.getModel('humanoid.armor')
            model2.head.showModel = self.__helmet
            model2.body.showModel = self.__armor
            model2.rightArm.showModel = self.__armor
            model2.leftArm.showModel = self.__armor
            model2.rightLeg.showModel = False
            model2.leftLeg.showModel = False
            model2.head.yRot = model.head.yRot
            model2.head.xRot = model.head.xRot
            model2.rightArm.xRot = model.rightArm.xRot
            model2.rightArm.zRot = model.rightArm.zRot
            model2.leftArm.xRot = model.leftArm.xRot
            model2.leftArm.zRot = model.leftArm.zRot
            model2.rightLeg.xRot = model.rightLeg.xRot
            model2.leftLeg.xRot = model.leftLeg.xRot
            model2.head.render(rotZ)
            model2.body.render(rotZ)
            model2.rightArm.render(rotZ)
            model2.leftArm.render(rotZ)
            model2.rightLeg.render(rotZ)
            model2.leftLeg.render(rotZ)
            gl.glEnable(gl.GL_CULL_FACE)

        gl.glDisable(gl.GL_ALPHA_TEST)
