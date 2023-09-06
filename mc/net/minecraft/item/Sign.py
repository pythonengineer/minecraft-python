from mc.net.minecraft.Entity import Entity
from mc.net.minecraft.item.SignModel import SignModel
from pyglet import gl
import math

class Sign(Entity):
    __model = SignModel()

    def __init__(self, level, x, y, z, rot):
        super().__init__(level)
        self.__messages = ['This is a test', 'of the signs.', 'Each line can', 'be 15 chars!']
        self.setSize(0.5, 1.5)
        self.heightOffset = self.bbHeight / 2.0
        self.setPos(x, y, z)
        self.__rot = -rot
        self.heightOffset = 1.5
        self.__xd = -(math.sin(self.__rot * math.pi / 180.0)) * 0.05
        self.__yd = 0.2
        self.__zd = -(math.cos(self.__rot * math.pi / 180.0)) * 0.05
        self.makeStepSound = False

    def isPickable(self):
        return not self.removed

    def tick(self):
        self.xo = self.x
        self.yo = self.y
        self.zo = self.z
        self.__yd -= 0.04
        self.move(self.__xd, self.__yd, self.__zd)
        self.__xd *= 0.98
        self.__yd *= 0.98
        self.__zd *= 0.98
        if self.onGround:
            self.__xd *= 0.7
            self.__zd *= 0.7
            self.__yd *= -0.5

    def render(self, textures, translation):
        gl.glEnable(gl.GL_TEXTURE_2D)
        tex = textures.loadTexture('item/sign.png')
        gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
        f2 = self.level.getBrightness(self.x, self.y, self.z)
        gl.glPushMatrix()
        gl.glColor4f(f2, f2, f2, 1.0)
        gl.glTranslatef(self.xo + (self.x - self.xo) * translation,
                        self.yo + (self.y - self.yo) * translation - self.heightOffset / 2.0,
                        self.zo + (self.z - self.zo) * translation)
        gl.glRotatef(self.__rot, 0.0, 1.0, 0.0)
        gl.glPushMatrix()
        gl.glScalef(1.0, -1.0, -1.0)
        self.__model.signBoard.render(0.0625)
        self.__model.signStick.render(0.0625)
        gl.glPopMatrix()
        f3 = 0.016666668
        gl.glTranslatef(0.0, 0.5, 0.09)
        gl.glScalef(f3, -f3, f3)
        gl.glNormal3f(0.0, 0.0, -1.0 * f3)
        gl.glEnable(gl.GL_BLEND)
        for i in range(len(self.__messages)):
            string = self.__messages[i]
            self.level.font.draw(string, -self.level.font.width(string) // 2,
                                 i * 10 - len(self.__messages) * 5, 0x202020)
        gl.glDisable(gl.GL_BLEND)
        gl.glDisable(gl.GL_TEXTURE_2D)
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        gl.glPopMatrix()
