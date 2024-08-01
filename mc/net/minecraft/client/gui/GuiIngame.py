from mc.net.minecraft.client.render.entity.RenderItem import RenderItem
from mc.net.minecraft.client.gui.ScaledResolution import ScaledResolution
from mc.net.minecraft.client.gui.Gui import Gui
from mc.net.minecraft.client.RenderHelper import RenderHelper
from mc.JavaUtils import Random
from pyglet import window, gl
import math

class GuiIngame(Gui):
    __itemRenderer = RenderItem()
    __rand = Random()

    def __init__(self, minecraft):
        self.__mc = minecraft
        self.__chatMessageList = []
        self.__updateCounter = 0

    def renderGameOverlay(self, a):
        scaledRes = ScaledResolution(self.__mc.width, self.__mc.height)
        scaledWidth = scaledRes.getScaledWidth()
        scaledHeight = scaledRes.getScaledHeight()
        self.__mc.entityRenderer.setupOverlayRendering()
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.__mc.renderEngine.getTexture('gui/gui.png'))
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        gl.glEnable(gl.GL_BLEND)
        self._zLevel = -90.0
        self.drawTexturedModalRect(scaledWidth / 2 - 91, scaledHeight - 22, 0, 0, 182, 22)
        self.drawTexturedModalRect(scaledWidth / 2 - 91 - 1 + self.__mc.thePlayer.inventory.currentItem * 20,
                                   scaledHeight - 22 - 1, 0, 22, 24, 22)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.__mc.renderEngine.getTexture('gui/icons.png'))
        self.drawTexturedModalRect(scaledWidth / 2 - 7, scaledHeight / 2 - 7, 0, 0, 16, 16)
        invulnerable = self.__mc.thePlayer.heartsLife / 3 % 2 == 1
        if self.__mc.thePlayer.heartsLife < 10:
            invulnerable = False

        health = self.__mc.thePlayer.health
        prevHealth = self.__mc.thePlayer.prevHealth
        self.__rand.setSeed(self.__updateCounter * 312871)
        if self.__mc.playerController.shouldDrawHUD():
            for i in range(10):
                x = scaledWidth / 2 - 91 + (i << 3)
                y = scaledHeight - 32
                if health <= 4:
                    y += self.__rand.nextInt(2)

                self.drawTexturedModalRect(x, y, 16 + invulnerable * 9, 0, 9, 9)
                if invulnerable:
                    if (i << 1) + 1 < prevHealth:
                        self.drawTexturedModalRect(x, y, 70, 0, 9, 9)
                    elif (i << 1) + 1 == prevHealth:
                        self.drawTexturedModalRect(x, y, 79, 0, 9, 9)

                if (i << 1) + 1 < health:
                    self.drawTexturedModalRect(x, y, 52, 0, 9, 9)
                elif (i << 1) + 1 == health:
                    self.drawTexturedModalRect(x, y, 61, 0, 9, 9)

            if self.__mc.thePlayer.isInsideOfMaterial():
                bubbles = math.ceil((self.__mc.thePlayer.air - 2) * 10.0 / 300.0)
                rem = math.ceil(self.__mc.thePlayer.air * 10.0 / 300.0) - bubbles
                for i in range(bubbles + rem):
                    if i < bubbles:
                        self.drawTexturedModalRect(scaledWidth / 2 - 91 + (i << 3),
                                                   scaledHeight - 32 - 9, 16, 18, 9, 9)
                    else:
                        self.drawTexturedModalRect(scaledWidth / 2 - 91 + (i << 3),
                                                   scaledHeight - 32 - 9, 25, 18, 9, 9)

        gl.glDisable(gl.GL_BLEND)
        gl.glEnable(gl.GL_NORMALIZE)
        gl.glPushMatrix()
        gl.glRotatef(180.0, 1.0, 0.0, 0.0)
        RenderHelper.enableStandardItemLighting()
        gl.glPopMatrix()

        for slot in range(9):
            width = scaledWidth // 2 - 90 + slot * 20 + 2
            height = scaledHeight - 16 - 3
            stack = self.__mc.thePlayer.inventory.mainInventory[slot]
            if stack:
                anim = stack.animationsToGo - a
                if anim > 0.0:
                    gl.glPushMatrix()
                    s = 1.0 + anim / 5.0
                    gl.glTranslatef(width + 8, height + 12, 0.0)
                    gl.glScalef(1.0 / s, (s + 1.0) / 2.0, 1.0)
                    gl.glTranslatef(-(width + 8), -(height + 12), 0.0)

                self.__itemRenderer.renderItemIntoGUI(
                    self.__mc.renderEngine,
                    stack, width, height
                )
                if anim > 0.0:
                    gl.glPopMatrix()

                self.__itemRenderer.renderItemDamage(
                    self.__mc.fontRenderer,
                    stack, width, height
                )

        RenderHelper.disableStandardItemLighting()
        gl.glDisable(gl.GL_NORMALIZE)
        self.__mc.fontRenderer.drawStringWithShadow(self.__mc.VERSION_STRING, 2, 2, 0xFFFFFF)
        if self.__mc.options.showFPS:
            self.__mc.fontRenderer.drawStringWithShadow(self.__mc.debug, 2, 12, 0xFFFFFF)
            self.__mc.fontRenderer.drawStringWithShadow(
                'E: ' + self.__mc.theWorld.getDebugLoadedEntities() + '. P: ' + \
                self.__mc.effectRenderer.getStatistics() + '. LT: ' + \
                self.__mc.theWorld.getDebugMapInfo(), 2, 22, 0xFFFFFF
            )

        for i, message in enumerate(self.__chatMessageList):
            if i >= 10:
                break

            if message.updateCounter < 200:
                self.__mc.fontRenderer.drawStringWithShadow(
                    None, 2, scaledHeight - 8 - i * 9 - 20, 0xFFFFFF
                )

    def addChatMessage(self):
        self.__updateCounter += 1
        for message in self.__chatMessageList.copy():
            message.updateCounter += 1
