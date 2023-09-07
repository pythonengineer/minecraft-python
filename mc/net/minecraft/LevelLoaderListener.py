from mc.net.minecraft import StopGameException
from mc.net.minecraft.renderer.Tesselator import tesselator
from pyglet import clock, gl

class LevelLoaderListener:

    def __init__(self, minecraft):
        self.__minecraft = minecraft
        self.__title = ''
        self.__desc = ''

    def beginLevelLoading(self, desc):
        if not self.__minecraft.running:
            raise StopGameException
        else:
            self.__desc = desc
            screenWidth = self.__minecraft.width * 240 / self.__minecraft.height
            screenHeight = self.__minecraft.height * 240 / self.__minecraft.height

            gl.glClear(gl.GL_DEPTH_BUFFER_BIT)
            gl.glMatrixMode(gl.GL_PROJECTION)
            gl.glLoadIdentity()
            gl.glOrtho(0.0, screenWidth, screenHeight, 0.0, 100.0, 300.0)
            gl.glMatrixMode(gl.GL_MODELVIEW)
            gl.glLoadIdentity()
            gl.glTranslatef(0.0, 0.0, -200.0)

    def levelLoadUpdate(self, title):
        if not self.__minecraft.running:
            raise StopGameException
        else:
            self.__title = title
            self.setLoadingProgress()

    def setLoadingProgress(self):
        if not self.__minecraft.running:
            raise StopGameException
        else:
            screenWidth = self.__minecraft.width * 240 // self.__minecraft.height
            screenHeight = self.__minecraft.height * 240 // self.__minecraft.height

            gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

            t = tesselator
            id_ = self.__minecraft.textures.loadTexture('dirt.png')
            gl.glBindTexture(gl.GL_TEXTURE_2D, id_)
            s = 32.0
            t.begin()
            t.color(0x404040)
            t.vertexUV(0.0, screenHeight, 0.0, 0.0, screenHeight / s)
            t.vertexUV(screenWidth, screenHeight, 0.0, screenWidth / s, screenHeight / s)
            t.vertexUV(screenWidth, 0.0, 0.0, screenWidth / s, 0.0)
            t.vertexUV(0.0, 0.0, 0.0, 0.0, 0.0)
            t.end()

            self.__minecraft.font.drawShadow(self.__desc, (screenWidth - self.__minecraft.font.width(self.__desc)) // 2, screenHeight // 2 - 4 - 16, 0xFFFFFF)
            self.__minecraft.font.drawShadow(self.__title, (screenWidth - self.__minecraft.font.width(self.__title)) // 2, screenHeight // 2 - 4 + 8, 0xFFFFFF)
            clock.tick()
            self.__minecraft.flip()
