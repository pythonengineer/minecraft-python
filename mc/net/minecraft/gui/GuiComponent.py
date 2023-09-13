from mc.net.minecraft.renderer.Tesselator import tesselator
from mc.CompatibilityShims import rshift
from pyglet import gl

class GuiComponent:
    _blitOffset = 0.0

    @staticmethod
    def _fill(x0, y0, x1, y1, col):
        a = rshift(col, 24) / 255.0
        r = (col >> 16 & 255) / 255.0
        g = (col >> 8 & 255) / 255.0
        b = (col & 255) / 255.0
        t = tesselator
        gl.glEnable(gl.GL_BLEND)
        gl.glDisable(gl.GL_TEXTURE_2D)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glColor4f(r, g, b, a)
        t.begin()
        t.vertex(x0, y1, 0.0)
        t.vertex(x1, y1, 0.0)
        t.vertex(x1, y0, 0.0)
        t.vertex(x0, y0, 0.0)
        t.end()
        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glDisable(gl.GL_BLEND)

    @staticmethod
    def _fillGradient(x0, y0, x1, y1, col1, col2):
        f10 = rshift(col1, 24) / 255.0
        f11 = (col1 >> 16 & 255) / 255.0
        f6 = (col1 >> 8 & 255) / 255.0
        f12 = (col1 & 255) / 255.0
        f7 = rshift(col2, 24) / 255.0
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
        font.drawShadow(string, x - font.width(string) // 2, y, color)

    @staticmethod
    def drawString(font, string, x, y, color):
        font.drawShadow(string, x, y, color)

    def blit(self, i1, i2, i3, i4, i5, i6):
        f7 = 0.00390625
        f8 = 0.00390625
        t = tesselator
        t.begin()
        t.vertexUV(i1, i2 + i6, self._blitOffset, i3 * f7, (i4 + i6) * f8)
        t.vertexUV(i1 + i5, i2 + i6, self._blitOffset, (i3 + i5) * f7, (i4 + i6) * f8)
        t.vertexUV(i1 + i5, i2, self._blitOffset, (i3 + i5) * f7, i4 * f8)
        t.vertexUV(i1, i2, self._blitOffset, i3 * f7, i4 * f8)
        t.end()
