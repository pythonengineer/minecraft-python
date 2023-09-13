from mc.net.minecraft.net.NetworkPlayerTextureLoader import NetworkPlayerTextureLoader
from mc.net.minecraft.mob.HumanoidMob import HumanoidMob
from mc.net.minecraft.net.EntityPos import EntityPos
from mc.net.minecraft.gui.Font import Font
from mc.CompatibilityShims import rshift
from collections import deque
from pyglet import gl

class NetworkPlayer(HumanoidMob):

    def __init__(self, minecraft, i, name, xp, yp, zp, yRot, xRot):
        super().__init__(minecraft.level, xp, yp, zp)
        self.__minecraft = minecraft
        self.displayName = name
        self.name = Font.removeColorCodes(name)
        self.tickCount = 0
        self.__xp = xp
        self.__yp = yp
        self.__zp = zp
        self.heightOffset = 0.0
        self.pushthrough = 0.8
        self.__moveQueue = deque()
        self.__texture = -1
        self.newTexture = None
        self.__textures = None
        self.setPos(xp / 32.0, yp / 32.0, zp / 32.0)
        self.xRot = xRot
        self.yRot = yRot
        self.armor = self.helmet = False
        NetworkPlayerTextureLoader(self).start()
        self.allowAlpha = False

    def aiStep(self):
        i = 5
        while True:
            if len(self.__moveQueue) > 0:
                self.setMovePos(self.__moveQueue.popleft())

            i -= 1
            if i + 1 <= 0 or len(self.__moveQueue) <= 10:
                break

        self.onGround = True

    def bindTexture(self, textures):
        if self.newTexture:
            hasHair = False

            if self.newTexture.height > 32:
                self.newTexture.crop((0, 32, 64, 32))

            rgb = list(self.newTexture.getdata())
            argb = bytearray(512)

            def convertPixel(c):
                x = c[0] << 16 | c[1] << 8 | c[2] | c[3] << 24
                if x >= 1 << 31:
                    x -= 1 << 32

                return x

            argb = [convertPixel(pixel) for pixel in rgb]

            for i in range(512):
                a = rshift(argb[i], 24)
                r = argb[i] >> 16 & 255
                g = argb[i] >> 8 & 255
                b = argb[i] & 255
                if a < 128:
                    hasHair = True
                    break

            self.hasHair = hasHair
            self.__texture = textures.loadTextureImg(self.newTexture)
            self.newTexture = None

        if self.__texture < 0:
            gl.glBindTexture(gl.GL_TEXTURE_2D, self.__textures.loadTexture('char.png'))
        else:
            gl.glBindTexture(gl.GL_TEXTURE_2D, self.__texture)

    def render(self, textures, translation):
        self.__textures = textures
        super().render(textures, translation)
        gl.glPushMatrix()
        f = 0.05
        gl.glTranslatef(self.xo + (self.x - self.xo) * translation,
                        self.yo + (self.y - self.yo) * translation + 0.8,
                        self.zo + (self.z - self.zo) * translation)
        gl.glRotatef(-self.__minecraft.player.yRot, 0.0, 1.0, 0.0)
        gl.glScalef(f, -f, f)
        gl.glTranslatef(-self.__minecraft.font.width(self.displayName) / 2.0, 0.0, 0.0)
        gl.glNormal3f(1.0, -1.0, 1.0)
        gl.glDisable(gl.GL_LIGHTING)
        gl.glDisable(gl.GL_LIGHT0)
        if self.name.lower() == 'notch':
            self.__minecraft.font.draw(self.displayName, 0, 0, 16776960)
        else:
            self.__minecraft.font.draw(self.displayName, 0, 0, 16777215)

        gl.glEnable(gl.GL_LIGHT0)
        gl.glEnable(gl.GL_LIGHTING)
        gl.glTranslatef(1.0, 1.0, -0.05)
        self.__minecraft.font.draw(self.name, 0, 0, 5263440)
        gl.glPopMatrix()

    def queue1(self, xa, ya, za, xr, yr):
        rotX = xr - self.yRot
        rotY = yr - self.xRot
        while rotX >= 180.0:
            rotX -= 360.0

        while rotX < -180.0:
            rotX += 360.0

        while rotY >= 180.0:
            rotY -= 360.0

        while rotY < -180.0:
            rotY += 360.0

        rotX = self.yRot + rotX * 0.5
        rotY = self.xRot + rotY * 0.5
        self.__moveQueue.append(EntityPos((self.__xp + xa / 2.0) / 32.0,
                                          (self.__yp + ya / 2.0) / 32.0,
                                          (self.__zp + za / 2.0) / 32.0, rotX, rotY))
        self.__xp += xa
        self.__yp += ya
        self.__zp += za
        self.__moveQueue.append(EntityPos(self.__xp / 32.0,
                                          self.__yp / 32.0,
                                          self.__zp / 32.0, xr, yr))

    def teleport(self, xa, ya, za, rotX, rotZ):
        xr = rotX - self.yRot
        zr = rotZ - self.xRot
        while xr >= 180.0:
            xr -= 360.0

        while xr < -180.0:
            xr += 360.0

        while zr >= 180.0:
            zr -= 360.0

        while zr < -180.0:
            zr += 360.0

        xr = self.yRot + xr * 0.5
        zr = self.xRot + zr * 0.5
        self.__moveQueue.append(EntityPos((self.__xp + xa) / 64.0,
                                          (self.__yp + ya) / 64.0,
                                          (self.__zp + za) / 64.0, xr, zr))
        self.__xp = xa
        self.__yp = ya
        self.__zp = za
        self.__moveQueue.append(EntityPos(self.__xp / 32.0,
                                          self.__yp / 32.0,
                                          self.__zp / 32.0, rotX, rotZ))

    def queue3(self, xa, ya, za):
        self.__moveQueue.append(EntityPos((self.__xp + xa / 2.0) / 32.0,
                                          (self.__yp + ya / 2.0) / 32.0,
                                          (self.__zp + za / 2.0) / 32.0))
        self.__xp += xa
        self.__yp += ya
        self.__zp += za
        self.__moveQueue.append(EntityPos(self.__xp / 32.0,
                                          self.__yp / 32.0,
                                          self.__zp / 32.0))

    def queue2(self, rotX, rotY):
        xr = rotX - self.yRot
        yr = rotY - self.xRot
        while xr >= 180.0:
            xr -= 360.0

        while xr < -180.0:
            xr += 360.0

        while yr >= 180.0:
            yr -= 360.0

        while yr < -180.0:
            yr += 360.0

        xr = self.yRot + xr * 0.5
        yr = self.xRot + yr * 0.5
        self.__moveQueue.append(EntityPos(xr, yr))
        self.__moveQueue.append(EntityPos(rotX, rotY))

    def clear(self):
        if self.__texture >= 0:
            del self.__textures.pixelsMap[self.__texture]
            self.__textures.ib.clear()
            self.__textures.ib.put(self.__texture)
            self.__textures.ib.flip()
            gl.glDeleteTextures(self.__textures.ib.capacity(), self.__textures.ib)
