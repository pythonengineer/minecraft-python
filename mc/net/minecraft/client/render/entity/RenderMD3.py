from mc.net.minecraft.client.model.md3.MD3Loader import MD3Loader
from mc.net.minecraft.client.model.md3.MD3Model import MD3Model
from mc.net.minecraft.client.render.entity.Render import Render
from pyglet import gl

class RenderMD3(Render):

    def __init__(self):
        super().__init__()
        self.__model = [None]
        self._shadowSize = 0.5

        try:
            self.__model[0] = MD3Model((MD3Loader()).loadModel('mcexport01.MD3'))
            print('Animation frames:', self.__model[0].getFrames())
        except IOError as e:
            print(e)

    def doRender(self, entity, xd, yd, zd, yaw, a):
        gl.glPushMatrix()

        try:
            zo = entity.prevRenderYawOffset + (entity.renderYawOffset - entity.prevRenderYawOffset) * a
            gl.glTranslatef(xd, yd, zd)
            if entity.mobType == 0:
                self._loadTexture('mcexport2.png')
            elif entity.mobType == 1:
                self._loadTexture('mcexport.png')

            gl.glRotatef(-zo + 180.0, 0.0, 1.0, 0.0)
            gl.glRotatef(-90.0, 1.0, 0.0, 0.0)
            gl.glScalef(0.02, -0.02, 0.02)
            ticks = (entity.ticksExisted + a) * entity.randVal
            a = int(ticks) % self.__model[0].getFrames()
            _ = (a + 1) % self.__model[0].getFrames()
            ticks -= int(ticks)
            gl.glEnable(gl.GL_NORMALIZE)
            self.__model[0].renderModelVertices(a, _, ticks)
            gl.glDisable(gl.GL_NORMALIZE)
        except Exception as e:
            print(e)

        gl.glPopMatrix()
