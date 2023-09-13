from mc.net.minecraft.gamemode.SurvivalGameMode import SurvivalGameMode
from mc.net.minecraft.renderer.Tesselator import tesselator
from mc.net.minecraft.gui.GuiComponent import GuiComponent
from mc.net.minecraft.gui.ChatScreen import ChatScreen
from mc.net.minecraft.level.tile.Tiles import tiles
from mc.net.minecraft.GuiMessage import GuiMessage
from pyglet import window, gl
from random import Random
import math

class Gui(GuiComponent):
    __rand = Random()

    def __init__(self, minecraft, width, height):
        self.__minecraft = minecraft
        self.__scaledWidth = width * 240 // height
        self.__scaledHeight = height * 240 // height
        self.messages = []
        self.hoveredUsername = None
        self.tickCounter = 0

    def render(self, scale, playerAlive, xm, ym):
        self.__minecraft.gameRenderer.render()
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.__minecraft.textures.loadTexture('gui/gui.png'))
        t = tesselator
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        gl.glEnable(gl.GL_BLEND)
        self._blitOffset = -90.0
        self.blit(self.__scaledWidth / 2 - 91, self.__scaledHeight - 22, 0, 0, 182, 22)
        self.blit(self.__scaledWidth / 2 - 91 - 1 + self.__minecraft.player.inventory.selected * 20,
                  self.__scaledHeight - 22 - 1, 0, 22, 24, 22)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.__minecraft.textures.loadTexture('gui/icons.png'))
        self.blit(self.__scaledWidth / 2 - 7, self.__scaledHeight / 2 - 7, 0, 0, 16, 16)
        invulnerable = 1 if self.__minecraft.player.invulnerableTime // 3 % 2 == 1 else 0
        if self.__minecraft.player.invulnerableTime < 10:
            invulnerable = 0

        health = self.__minecraft.player.health
        prevHealth = self.__minecraft.player.lastHealth
        self.__rand.seed(self.tickCounter * 312871)
        if self.__minecraft.gamemode.canHurtPlayer():
            for i in range(10):
                n5 = 0
                if invulnerable != 0:
                    n5 = 1

                n4 = self.__scaledWidth / 2 - 91 + (i << 3)
                n3 = self.__scaledHeight - 32
                if health <= 4:
                    n3 += self.__rand.randint(0, 1)

                self.blit(n4, n3, 16 + n5 * 9, 0, 9, 9)
                if invulnerable != 0:
                    if (i << 1) + 1 < prevHealth:
                        self.blit(n4, n3, 70, 0, 9, 9)

                    if (i << 1) + 1 == prevHealth:
                        self.blit(n4, n3, 79, 0, 9, 9)

                if (i << 1) + 1 < health:
                    self.blit(n4, n3, 52, 0, 9, 9)

                if (i << 1) + 1 != health:
                    continue

                self.blit(n4, n3, 61, 0, 9, 9)

            if self.__minecraft.player.isUnderWater():
                n6 = math.ceil((self.__minecraft.player.airSupply - 2) * 10.0 / 300.0)
                n5 = math.ceil(self.__minecraft.player.airSupply * 10.0 / 300.0) - n6
                for n4 in range(n6 + n5):
                    if n4 < n6:
                        self.blit(self.__scaledWidth / 2 - 91 + (n4 << 3),
                                  self.__scaledHeight - 32 - 9, 16, 18, 9, 9)
                        continue

                    self.blit(self.__scaledWidth / 2 - 91 + (n4 << 3),
                              self.__scaledHeight - 32 - 9, 25, 18, 9, 9)

        gl.glDisable(gl.GL_BLEND)

        for slot in range(len(self.__minecraft.player.inventory.slots)):
            width = self.__scaledWidth // 2 - 90 + slot * 20
            height = self.__scaledHeight - 16
            tile = self.__minecraft.player.inventory.slots[slot]
            if tile <= 0:
                continue

            gl.glPushMatrix()
            gl.glTranslatef(width, height, -50.0)
            if self.__minecraft.player.inventory.popTime[slot] > 0:
                f2 = (self.__minecraft.player.inventory.popTime[slot] - scale) / 5.0
                f3 = -(math.sin((f2 * f2) * math.pi)) * 8.0
                f4 = math.sin((f2 * f2) * math.pi) + 1.0
                f5 = math.sin(f2 * math.pi) + 1.0
                gl.glTranslatef(10.0, f3 + 10.0, 0.0)
                gl.glScalef(f4, f5, 1.0)
                gl.glTranslatef(-10.0, -10.0, 0.0)

            gl.glScalef(10.0, 10.0, 10.0)
            gl.glTranslatef(1.0, 0.5, 0.0)
            gl.glRotatef(-30.0, 1.0, 0.0, 0.0)
            gl.glRotatef(45.0, 0.0, 1.0, 0.0)
            gl.glTranslatef(-1.5, 0.5, 0.5)
            gl.glScalef(-1.0, -1.0, -1.0)
            tex = self.__minecraft.textures.loadTexture('terrain.png')
            gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
            t.begin()
            tiles.tiles[tile].render(t)
            t.end()
            gl.glPopMatrix()
            if self.__minecraft.player.inventory.count[slot] > 1:
                string = '' + str(self.__minecraft.player.inventory.count[slot])
                self.__minecraft.font.drawShadow(string,
                                                 width + 19 - self.__minecraft.font.width(string),
                                                 height + 6, 0xFFFFFF)

        self.__minecraft.font.drawShadow(self.__minecraft.VERSION_STRING, 2, 2, 0xFFFFFF)
        if self.__minecraft.options.showFramerate:
            self.__minecraft.font.drawShadow(self.__minecraft.fpsString, 2, 12, 0xFFFFFF)

        if isinstance(self.__minecraft.gamemode, SurvivalGameMode):
            score = 'Score: &e' + str(self.__minecraft.player.getScore())
            self.__minecraft.font.drawShadow(score,
                                             self.__scaledWidth - self.__minecraft.font.width(score) - 2,
                                             2, 16777215)
            self.__minecraft.font.drawShadow('Arrows: ' + str(self.__minecraft.player.arrows),
                                             self.__scaledWidth // 2 + 8, self.__scaledHeight - 33, 16777215)

        b13 = 10
        z5 = False
        if isinstance(self.__minecraft.guiScreen, ChatScreen):
            b13 = 20
            z5 = True

        for i, message in enumerate(self.messages):
            if i >= b13:
                break

            if message.counter < 200 or z5:
                self.__minecraft.font.drawShadow(message.message, 2, self.__scaledHeight - 8 - i * 9 - 20, 0xFFFFFF)

        screenWidth = self.__scaledWidth // 2
        screenHeight = self.__scaledHeight // 2
        self.hoveredUsername = None
        if self.__minecraft.ksh[window.key.TAB] and self.__minecraft.networkClient and self.__minecraft.networkClient.isConnected():
            players = self.__minecraft.networkClient.getUsernames()
            gl.glEnable(gl.GL_BLEND)
            gl.glDisable(gl.GL_TEXTURE_2D)
            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
            gl.glBegin(gl.GL_QUADS)
            gl.glColor4f(0.0, 0.0, 0.0, 0.7)
            gl.glVertex2f(screenWidth + 128, screenHeight - 68 - 12)
            gl.glVertex2f(screenWidth - 128, screenHeight - 68 - 12)
            gl.glColor4f(0.2, 0.2, 0.2, 0.8)
            gl.glVertex2f(screenWidth - 128, screenHeight + 68)
            gl.glVertex2f(screenWidth + 128, screenHeight + 68)
            gl.glEnd()
            gl.glDisable(gl.GL_BLEND)
            gl.glEnable(gl.GL_TEXTURE_2D)
            string = 'Connected players:'
            self.__minecraft.font.drawShadow(string, screenWidth - self.__minecraft.font.width(string) // 2, screenHeight - 64 - 12, 0xFFFFFF)

            for i, name in enumerate(players):
                width = screenWidth + i % 2 * 120 - 120
                height = screenHeight - 64 + (i // 2 << 3)
                if playerAlive and xm >= width and ym >= height and xm < width + 120 and ym < height + 8:
                    self.hoveredUsername = name
                    self.__minecraft.font.draw(name, width + 2, height, 0xFFFFFF)
                else:
                    self.__minecraft.font.draw(name, width, height, 0xFFFFFF)

    def addMessage(self, string):
        self.messages.insert(0, GuiMessage(string))

        while len(self.messages) > 50:
            self.messages.pop(len(self.messages) - 1)
