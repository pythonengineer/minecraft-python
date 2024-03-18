from mc.net.minecraft.client import MinecraftError
from mc.net.minecraft.client.render.Tessellator import tessellator
from pyglet import clock, gl

class LoadingScreenRenderer:

    def __init__(self, minecraft):
        self.minecraft = minecraft
        self.__text = ''
        self.title = ''

    def beginLevelLoading(self, title):
        if not self.minecraft.running:
            raise MinecraftError
        else:
            self.title = title
            screenWidth = self.minecraft.width * 240 / self.minecraft.height
            screenHeight = self.minecraft.height * 240 / self.minecraft.height

            gl.glClear(gl.GL_DEPTH_BUFFER_BIT)
            gl.glMatrixMode(gl.GL_PROJECTION)
            gl.glLoadIdentity()
            gl.glOrtho(0.0, screenWidth, screenHeight, 0.0, 100.0, 300.0)
            gl.glMatrixMode(gl.GL_MODELVIEW)
            gl.glLoadIdentity()
            gl.glTranslatef(0.0, 0.0, -200.0)

    def displayProgressMessage(self, text):
        if not self.minecraft.running:
            raise MinecraftError
        else:
            self.__text = text
            self.setLoadingProgress()

    def setLoadingProgress(self):
        if not self.minecraft.running:
            raise MinecraftError
        else:
            screenWidth = self.minecraft.width * 240 // self.minecraft.height
            screenHeight = self.minecraft.height * 240 // self.minecraft.height

            gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

            t = tessellator
            id_ = self.minecraft.renderEngine.getTexture('dirt.png')
            gl.glBindTexture(gl.GL_TEXTURE_2D, id_)
            s = 32.0
            t.startDrawingQuads()
            t.setColorOpaque_I(0x404040)
            t.addVertexWithUV(0.0, screenHeight, 0.0, 0.0, screenHeight / s)
            t.addVertexWithUV(screenWidth, screenHeight, 0.0, screenWidth / s, screenHeight / s)
            t.addVertexWithUV(screenWidth, 0.0, 0.0, screenWidth / s, 0.0)
            t.addVertexWithUV(0.0, 0.0, 0.0, 0.0, 0.0)
            t.draw()

            self.minecraft.fontRenderer.drawStringWithShadow(
                self.title,
                (screenWidth - self.minecraft.fontRenderer.getWidth(self.title)) // 2,
                screenHeight // 2 - 4 - 16, 0xFFFFFF
            )
            self.minecraft.fontRenderer.drawStringWithShadow(
                self.__text,
                (screenWidth - self.minecraft.fontRenderer.getWidth(self.__text)) // 2,
                screenHeight // 2 - 4 + 8, 0xFFFFFF
            )

            clock.tick()
            self.minecraft.flip()
