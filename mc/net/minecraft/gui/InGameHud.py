from mc.net.minecraft.renderer.Tesselator import tesselator
from mc.net.minecraft.gui.ChatScreen import ChatScreen
from mc.net.minecraft.level.tile.Tiles import tiles
from mc.net.minecraft.ChatLine import ChatLine
from mc.net.minecraft.User import User
from pyglet import window, gl

class InGameHud:

    def __init__(self, minecraft, width, height):
        self.__minecraft = minecraft
        self.__scaledWidth = width * 240 // height
        self.__scaledHeight = height * 240 // height
        self.messages = []

    def render(self):
        self.__minecraft.renderHelper.initGui()
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.__minecraft.textures.getTextureId('gui.png'))
        gl.glEnable(gl.GL_TEXTURE_2D)
        t = tesselator
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        gl.glEnable(gl.GL_BLEND)
        self.__blit(self.__scaledWidth / 2 - 91, self.__scaledHeight - 22, 0, 0, 182, 22)
        self.__blit(self.__scaledWidth / 2 - 91 - 1 + self.__minecraft.player.inventory.selectedSlot * 20, self.__scaledHeight - 22 - 1, 0, 22, 24, 22)
        gl.glDisable(gl.GL_BLEND)

        for i in range(len(self.__minecraft.player.inventory.slots)):
            i6 = self.__minecraft.player.inventory.slots[i]
            if i6 > 0:
                gl.glPushMatrix()
                gl.glTranslatef(self.__scaledWidth / 2 - 90 + i * 20, self.__scaledHeight - 16, -50.0)
                gl.glScalef(10.0, 10.0, 10.0)
                gl.glTranslatef(1.0, 0.5, 0.0)
                gl.glRotatef(-30.0, 1.0, 0.0, 0.0)
                gl.glRotatef(45.0, 0.0, 1.0, 0.0)
                gl.glTranslatef(-1.5, 0.5, 0.5)
                gl.glScalef(-1.0, -1.0, -1.0)
                i7 = self.__minecraft.textures.getTextureId('terrain.png')
                gl.glBindTexture(gl.GL_TEXTURE_2D, i7)
                gl.glEnable(gl.GL_TEXTURE_2D)
                t.begin()
                tiles.tiles[i6].render(t, self.__minecraft.level, 0, -2, 0, 0)
                t.end()
                gl.glDisable(gl.GL_TEXTURE_2D)
                gl.glPopMatrix()

        self.__minecraft.font.drawShadow(self.__minecraft.VERSION_STRING, 2, 2, 16777215)
        self.__minecraft.font.drawShadow(self.__minecraft.fpsString, 2, 12, 16777215)

        b13 = 10
        z5 = False
        if isinstance(self.__minecraft.screen, ChatScreen):
            b13 = 20
            z5 = True

        for i, message in enumerate(self.messages):
            if i >= b13:
                break

            if message.counter < 200 or z5:
                self.__minecraft.font.drawShadow(message.message, 2, self.__scaledHeight - 8 - i * 9 - 20, 0xFFFFFF)

        screenWidth = self.__scaledWidth // 2
        screenHeight = self.__scaledHeight // 2
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        t.begin()
        t.vertex(screenWidth + 1, screenHeight - 4, 0.0)
        t.vertex(screenWidth - 0, screenHeight - 4, 0.0)
        t.vertex(screenWidth - 0, screenHeight + 5, 0.0)
        t.vertex(screenWidth + 1, screenHeight + 5, 0.0)
        t.vertex(screenWidth + 5, screenHeight - 0, 0.0)
        t.vertex(screenWidth - 4, screenHeight - 0, 0.0)
        t.vertex(screenWidth - 4, screenHeight + 1, 0.0)
        t.vertex(screenWidth + 5, screenHeight + 1, 0.0)
        t.end()
        if self.__minecraft.ksh[window.key.TAB] and self.__minecraft.connectionManager and self.__minecraft.connectionManager.isConnected():
            players = []
            players.append(self.__minecraft.user.name)
            for player in self.__minecraft.connectionManager.players.values():
                players.append(player.name)

            gl.glEnable(gl.GL_BLEND)
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
            string = 'Connected players:'
            self.__minecraft.font.drawShadow(string, screenWidth - self.__minecraft.font.width(string) // 2, screenHeight - 64 - 12, 0xFFFFFF)

            for i, name in enumerate(players):
                i4 = screenWidth + i % 2 * 120 - 120
                i15 = screenHeight - 64 + (i // 2 << 3)
                self.__minecraft.font.draw(name, i4, i15, 0xFFFFFF)

    @staticmethod
    def __blit(i0, i1, i2, i3, i4, i5):
        f7 = 0.00390625
        f8 = 0.015625
        t = tesselator
        t.begin()
        t.vertexUV(i0, i1 + 22, -90.0, 0.0, (i3 + 22) * f8)
        t.vertexUV(i0 + i4, i1 + 22, -90.0, (i4 + 0) * f7, (i3 + 22) * f8)
        t.vertexUV(i0 + i4, i1, -90.0, (i4 + 0) * f7, i3 * f8)
        t.vertexUV(i0, i1, -90.0, 0.0, i3 * f8)
        t.end()

    def addChatMessage(self, string):
        self.messages.insert(0, ChatLine(string))

        while len(self.messages) > 50:
            self.messages.pop(len(self.messages) - 1)
