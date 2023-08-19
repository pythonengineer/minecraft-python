from mc.net.minecraft.net.NetworkSkinDownloadThread import NetworkSkinDownloadThread
from mc.net.minecraft.net.PlayerMove import PlayerMove
from mc.net.minecraft.Entity import Entity
from collections import deque
from pyglet import gl
import math

class NetworkPlayer(Entity):

    def __init__(self, minecraft, i, name, xp, yp, zp, yRot, xRot):
        super().__init__(minecraft.level)
        self.__minecraft = minecraft
        self.__zombieModel = minecraft.playerModel
        self.name = name
        self.tickCount = 0
        self.__xp = xp
        self.__yp = yp
        self.__zp = zp
        self.__animStep = 0.0
        self.__animStepO = 0.0
        self.__moveQueue = deque()
        self.__yBodyRot = 0.0
        self.__yBodyRotO = 0.0
        self.__oRun = 0.0
        self.__run = 0.0
        self.__skin = -1
        self.newTexture = None
        self.__textures = None
        self.setPos(xp / 32.0, yp / 32.0, zp / 32.0)
        self.xRot = xRot
        self.yRot = yRot
        self.heightOffset = 1.62
        NetworkSkinDownloadThread(self).start()

    def tick(self):
        super().tick()
        self.__animStepO = self.__animStep
        self.__yBodyRotO = self.__yBodyRot
        self.yRotO = self.yRot
        self.xRotO = self.xRot
        self.tickCount += 1
        i1 = 5

        while True:
            if len(self.__moveQueue) > 0:
                self.setPos(self.__moveQueue.popleft())
            i1 -= 1
            if i1 + 1 <= 0 or len(self.__moveQueue) <= 10:
                break

        f6 = self.x - self.xo
        f2 = self.z - self.zo
        f3 = math.sqrt(f6 * f6 + f2 * f2)
        f4 = self.__yBodyRot
        f5 = 0.0
        self.__oRun = self.__run
        f7 = 0.0
        if f3 != 0.0:
            f7 = 1.0
            f5 = f3 * 3.0
            f4 = -(math.atan2(f2, f6) * 180.0 / math.pi + 90.0)

        self.__run += (f7 - self.__run) * 0.3

        f6 = f4 - self.__yBodyRot
        while f6 < -180.0:
            f6 += 360.0

        while f6 >= 180.0:
            f6 -= 360.0

        self.__yBodyRot += f6 * 0.1
        f6 = self.yRot - self.__yBodyRot
        while f6 < -180.0:
            f6 += 360.0

        while f6 >= 180.0:
            f6 -= 360.0

        z7 = f6 < -90.0 or f6 >= 90.0
        if f6 < -75.0:
            f6 = -75.0

        if f6 >= 75.0:
            f6 = 75.0

        self.__yBodyRot = self.yRot - f6
        self.__yBodyRot += f6 * 0.1
        if z7:
            f5 = -f5

        while self.yRot - self.yRotO < -180.0:
            self.yRotO -= 360.0

        while self.yRot - self.yRotO >= 180.0:
            self.yRotO += 360.0

        while self.__yBodyRot - self.__yBodyRotO < -180.0:
            self.__yBodyRotO -= 360.0

        while self.__yBodyRot - self.__yBodyRotO >= 180.0:
            self.__yBodyRotO += 360.0

        while self.xRot - self.xRotO < -180.0:
            self.xRotO -= 360.0

        while self.xRot - self.xRotO >= 180.0:
            self.xRotO += 360.0

        self.__animStep += f5

    def render(self, textures, a):
        self.__textures = textures
        f3 = self.__oRun + (self.__run - self.__oRun) * a
        gl.glEnable(gl.GL_TEXTURE_2D)
        if self.newTexture:
            self.__skin = self.__textures.addTexture(self.newTexture)
            self.newTexture = None

        if self.__skin < 0:
            gl.glBindTexture(gl.GL_TEXTURE_2D, self.__textures.getTextureId('char.png'))
        else:
            gl.glBindTexture(gl.GL_TEXTURE_2D, self.__skin)

        while self.__yBodyRotO - self.__yBodyRot < -180.0:
            self.__yBodyRotO += 360.0

        while self.__yBodyRotO - self.__yBodyRot >= 180.0:
            self.__yBodyRotO -= 360.0

        f9 = self.__yBodyRotO + (self.__yBodyRot - self.__yBodyRotO) * a
        while self.xRotO - self.xRot < -180.0:
            self.xRotO += 360.0

        while self.xRotO - self.xRot >= 180.0:
            self.xRotO -= 360.0

        while self.yRotO - self.yRot < -180.0:
            self.yRotO += 360.0

        while self.yRotO - self.yRot >= 180.0:
            self.yRotO -= 360.0

        f4 = self.yRotO + (self.yRot - self.yRotO) * a
        f5 = self.xRotO + (self.xRot - self.xRotO) * a
        f4 = -(f4 - f9)
        gl.glPushMatrix()
        f6 = self.__animStepO + (self.__animStep - self.__animStepO) * a
        f7 = self.getBrightness()
        gl.glColor3f(f7, f7, f7)
        f7 = 0.0625
        f8 = -abs(math.cos(f6 * 0.6662)) * 5.0 * f3 - 23.0
        gl.glTranslatef(self.xo + (self.x - self.xo) * a, self.yo + (self.y - self.yo) * a - self.heightOffset, self.zo + (self.z - self.zo) * a)
        gl.glScalef(1.0, -1.0, 1.0)
        gl.glTranslatef(0.0, f8 * f7, 0.0)
        gl.glRotatef(f9, 0.0, 1.0, 0.0)
        gl.glDisable(gl.GL_ALPHA_TEST)
        gl.glScalef(-1.0, 1.0, 1.0)
        self.__zombieModel.render(f6, f3, self.tickCount + a, f4, f5, f7)
        gl.glEnable(gl.GL_ALPHA_TEST)
        gl.glPopMatrix()
        gl.glPushMatrix()
        gl.glTranslatef(self.xo + (self.x - self.xo) * a, self.yo + (self.y - self.yo) * a + 0.8, self.zo + (self.z - self.zo) * a)
        gl.glRotatef(-self.__minecraft.player.yRot, 0.0, 1.0, 0.0)
        f2 = 0.05
        gl.glScalef(0.05, -f2, f2)
        gl.glTranslatef(-self.__minecraft.font.width(self.name) / 2.0, 0.0, 0.0)
        gl.glNormal3f(1.0, -1.0, 1.0)
        gl.glDisable(gl.GL_LIGHTING)
        gl.glDisable(gl.GL_LIGHT0)
        if self.name.lower() == 'notch':
            self.__minecraft.font.draw(self.name, 0, 0, 16776960)
        else:
            self.__minecraft.font.draw(self.name, 0, 0, 0xFFFFFF)

        gl.glEnable(gl.GL_LIGHT0)
        gl.glEnable(gl.GL_LIGHTING)
        gl.glTranslatef(1.0, 1.0, -0.05)
        self.__minecraft.font.draw(self.name, 0, 0, 5263440)
        gl.glPopMatrix()
        gl.glDisable(gl.GL_TEXTURE_2D)

    def queue(self, b1, b2, b3=None, f4=None, f5=None):
        if b3 is None:
            f1 = b1
            f2 = b2
            f3 = f1 - self.yRot
            f4 = f2 - self.xRot
            while f3 >= 180.0:
                f3 -= 360.0

            while f3 < -180.0:
                f3 += 360.0

            while f4 >= 180.0:
                f4 -= 360.0

            while f4 < -180.0:
                f4 += 360.0

            f3 = self.yRot + f3 * 0.5
            f4 = self.xRot + f4 * 0.5
            self.__moveQueue.append(PlayerMove(f3, f4))
            self.__moveQueue.append(PlayerMove(f1, f2))
        elif f4 is None:
            self.__moveQueue.append(PlayerMove((self.__xp + b1 / 2.0) / 32.0,
                                               (self.__yp + b2 / 2.0) / 32.0,
                                               (self.__zp + b3 / 2.0) / 32.0))
            self.__xp += b1
            self.__yp += b2
            self.__zp += b3
            self.__moveQueue.append(PlayerMove(self.__xp / 32.0,
                                               self.__yp / 32.0,
                                               self.__zp / 32.0))
        else:
            f6 = f4 - self.yRot
            f7 = f5 - self.xRot
            while f6 >= 180.0:
                f6 -= 360.0

            while f6 < -180.0:
                f6 += 360.0

            while f7 >= 180.0:
                f7 -= 360.0

            while f7 < -180.0:
                f7 += 360.0

            f6 = self.yRot + f6 * 0.5
            f7 = self.xRot + f7 * 0.5
            self.__moveQueue.append(PlayerMove((self.__xp + b1 / 2.0) / 32.0,
                                               (self.__yp + b2 / 2.0) / 32.0,
                                               (self.__zp + b3 / 2.0) / 32.0, f6, f7))
            self.__xp += b1
            self.__yp += b2
            self.__zp += b3
            self.__moveQueue.append(PlayerMove(self.__xp / 32.0,
                                               self.__yp / 32.0,
                                               self.__zp / 32.0, f4, f5))

    def teleport(self, s1, s2, s3, f4, f5):
        f6 = f4 - self.yRot
        f7 = f5 - self.xRot
        while f6 >= 180.0:
            f6 -= 360.0

        while f6 < -180.0:
            f6 += 360.0

        while f7 >= 180.0:
            f7 -= 360.0

        while f7 < -180.0:
            f7 += 360.0

        f6 = self.yRot + f6 * 0.5
        f7 = self.xRot + f7 * 0.5
        self.__moveQueue.append(PlayerMove((self.__xp + s1) / 64.0,
                                           (self.__yp + s2) / 64.0,
                                           (self.__zp + s3) / 64.0, f6, f7))
        self.__xp = s1
        self.__yp = s2
        self.__zp = s3
        self.__moveQueue.append(PlayerMove(self.__xp / 32.0,
                                           self.__yp / 32.0,
                                           self.__zp / 32.0, f4, f5))

    def clear(self):
        if self.__skin >= 0:
            print('Releasing texture for', self.name)
            self.__textures.idBuffer.clear()
            self.__textures.idBuffer.put(self.__skin)
            self.__textures.idBuffer.flip()
            gl.glDeleteTextures(self.__textures.idBuffer.capacity(), self.__textures.idBuffer)
