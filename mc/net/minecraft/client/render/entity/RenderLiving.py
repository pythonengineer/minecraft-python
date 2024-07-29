from mc.net.minecraft.client.render.entity.Render import Render
from mc.net.minecraft.client.model.ModelBiped import ModelBiped
from pyglet import gl

import math

class RenderLiving(Render):

    def __init__(self):
        self.__mainModel = ModelBiped()
        self._shadowSize = 0.5

    def doRender(self, entity, xd, yd, zd, yaw, a):
        gl.glPushMatrix()
        try:
            renderYaw = entity.prevRenderYawOffset + (entity.renderYawOffset - entity.prevRenderYawOffset) * a
            rotationYaw = entity.prevRotationYaw + (entity.rotationYaw - entity.prevRotationYaw) * a
            rotationPitch = entity.prevRotationPitch + (entity.rotationPitch - entity.prevRotationPitch) * a
            gl.glTranslatef(xd, yd, zd)
            self._loadTexture(entity.texture)
            gl.glRotatef(180.0 - renderYaw, 0.0, 1.0, 0.0)
            if entity.deathTime > 0:
                fall = (entity.deathTime + a - 1.0) / 20.0 * 1.6
                fall = min(math.sqrt(fall), 1.0)
                gl.glRotatef(fall * 90.0, 1.0, 0.0, 0.0)

            gl.glScalef(-(1.0 / 16.0), -(1.0 / 16.0), 1.0 / 16.0)
            gl.glTranslatef(0.0, -24.0, 0.0)
            gl.glEnable(gl.GL_NORMALIZE)
            y = entity.moveStrafing + (entity.moveForward - entity.moveStrafing) * a
            x = entity.randomYawVelocity - entity.moveForward * (1.0 - a)
            y = min(y, 1.0)
            self.__mainModel.render(x, y, 0.0, rotationYaw - renderYaw,
                                    rotationPitch, 1.0)
            if entity.hurtTime > 0 or entity.deathTime > 0:
                gl.glDisable(gl.GL_TEXTURE_2D)
                gl.glColor4f(1.0, 0.0, 0.0, 0.5)
                gl.glEnable(gl.GL_BLEND)
                gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
                self.__mainModel.render(x, y, 0.0, rotationYaw - renderYaw,
                                        rotationPitch, 1.0)
                gl.glDisable(gl.GL_BLEND)
                gl.glEnable(gl.GL_TEXTURE_2D)

            gl.glDisable(gl.GL_NORMALIZE)
        except Exception as e:
            print(str(e))

        gl.glPopMatrix()
