from mc.net.minecraft.client import MinecraftError
from mc.net.minecraft.client.render.Tessellator import tessellator
from pyglet import clock, gl

class LoadingScreenRenderer:

    def __init__(self, minecraft):
        self.__mc = minecraft
        self.__text = ''
        self.__title = ''

    def displayProgressMessage(self, title):
        if not self.__mc.running:
            raise MinecraftError
        else:
            self.__title = title
            screenWidth = self.__mc.width * 240 / self.__mc.height
            screenHeight = self.__mc.height * 240 / self.__mc.height

            gl.glClear(gl.GL_DEPTH_BUFFER_BIT)
            gl.glMatrixMode(gl.GL_PROJECTION)
            gl.glLoadIdentity()
            gl.glOrtho(0.0, screenWidth, screenHeight, 0.0, 100.0, 300.0)
            gl.glMatrixMode(gl.GL_MODELVIEW)
            gl.glLoadIdentity()
            gl.glTranslatef(0.0, 0.0, -200.0)

    def displayLoadingString(self, text):
        if not self.__mc.running:
            raise MinecraftError
        else:
            self.__text = text
            self.setLoadingProgress()

    def setLoadingProgress(self):
        if not self.__mc.running:
            raise MinecraftError
        else:
            screenWidth = self.__mc.width * 240 // self.__mc.height
            screenHeight = self.__mc.height * 240 // self.__mc.height

            gl.glClear(gl.GL_DEPTH_BUFFER_BIT)
            gl.glMatrixMode(gl.GL_PROJECTION)
            gl.glLoadIdentity()
            gl.glOrtho(0.0, screenWidth, screenHeight, 0.0, 100.0, 300.0)
            gl.glMatrixMode(gl.GL_MODELVIEW)
            gl.glLoadIdentity()
            gl.glTranslatef(0.0, 0.0, -200.0)
            gl.glClear(gl.GL_DEPTH_BUFFER_BIT | gl.GL_COLOR_BUFFER_BIT)

            t = tessellator
            id_ = self.__mc.renderEngine.getTexture('dirt.png')
            gl.glBindTexture(gl.GL_TEXTURE_2D, id_)
            s = 32.0
            t.startDrawingQuads()
            t.setColorOpaque_I(0x404040)
            t.addVertexWithUV(0.0, screenHeight, 0.0, 0.0, screenHeight / s)
            t.addVertexWithUV(screenWidth, screenHeight, 0.0, screenWidth / s, screenHeight / s)
            t.addVertexWithUV(screenWidth, 0.0, 0.0, screenWidth / s, 0.0)
            t.addVertexWithUV(0.0, 0.0, 0.0, 0.0, 0.0)
            t.draw()

            self.__mc.fontRenderer.drawStringWithShadow(
                self.__title,
                (screenWidth - self.__mc.fontRenderer.getStringWidth(self.__title)) // 2,
                screenHeight // 2 - 4 - 16, 0xFFFFFF
            )
            self.__mc.fontRenderer.drawStringWithShadow(
                self.__text,
                (screenWidth - self.__mc.fontRenderer.getStringWidth(self.__text)) // 2,
                screenHeight // 2 - 4 + 8, 0xFFFFFF
            )

            clock.tick()
            self.__mc.flip()
