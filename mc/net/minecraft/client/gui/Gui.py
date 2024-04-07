from mc.net.minecraft.client.render.Tessellator import tessellator
from pyglet import gl

class Gui:
    _zLevel = 0.0

    @staticmethod
    def _drawRect(x0, y0, x1, y1, col):
        a = ((col % 0x100000000) >> 24) / 255.0
        r = (col >> 16 & 255) / 255.0
        g = (col >> 8 & 255) / 255.0
        b = (col & 255) / 255.0
        t = tessellator
        gl.glEnable(gl.GL_BLEND)
        gl.glDisable(gl.GL_TEXTURE_2D)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glColor4f(r, g, b, a)
        t.startDrawingQuads()
        t.addVertex(x0, y1, 0.0)
        t.addVertex(x1, y1, 0.0)
        t.addVertex(x1, y0, 0.0)
        t.addVertex(x0, y0, 0.0)
        t.draw()
        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glDisable(gl.GL_BLEND)

    @staticmethod
    def _drawGradientRect(x0, y0, x1, y1, col1, col2):
        f10 = ((col1 % 0x100000000) >> 24) / 255.0
        f11 = (col1 >> 16 & 255) / 255.0
        f6 = (col1 >> 8 & 255) / 255.0
        f12 = (col1 & 255) / 255.0
        f7 = ((col2 % 0x100000000) >> 24) / 255.0
        f8 = (col2 >> 16 & 255) / 255.0
        f9 = (col2 >> 8 & 255) / 255.0
        f13 = (col2 & 255) / 255.0
        gl.glDisable(gl.GL_TEXTURE_2D)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glBegin(gl.GL_QUADS)
        gl.glColor4f(f11, f6, f12, f10)
        gl.glVertex2f(x1, y0)
        gl.glVertex2f(x0, y0)
        gl.glColor4f(f8, f9, f13, f7)
        gl.glVertex2f(x0, y1)
        gl.glVertex2f(x1, y1)
        gl.glEnd()
        gl.glDisable(gl.GL_BLEND)
        gl.glEnable(gl.GL_TEXTURE_2D)

    @staticmethod
    def drawCenteredString(font, string, x, y, color):
        font.drawStringWithShadow(string, x - font.getStringWidth(string) // 2, y, color)

    @staticmethod
    def drawString(font, string, x, y, color):
        font.drawStringWithShadow(string, x, y, color)

    def drawTexturedModalRect(self, x, y, xOffset, yOffset, w, h):
        f = 0.00390625
        t = tessellator
        t.startDrawingQuads()
        t.addVertexWithUV(x, y + h, self._zLevel, xOffset * f, (yOffset + h) * f)
        t.addVertexWithUV(x + w, y + h, self._zLevel, (xOffset + w) * f, (yOffset + h) * f)
        t.addVertexWithUV(x + w, y, self._zLevel, (xOffset + w) * f, yOffset * f)
        t.addVertexWithUV(x, y, self._zLevel, xOffset * f, yOffset * f)
        t.draw()
