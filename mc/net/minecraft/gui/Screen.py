from mc.net.minecraft.renderer.Tesselator import tesselator
from pyglet import gl

class Screen:

    def render(self, xMouse, yMouse):
        pass

    def init(self, minecraft, width, height):
        self.minecraft = minecraft
        self.width = width
        self.height = height

    def _fill(self, x0, y0, x1, y1, col):
        a = (col >> 24 & 0xFF) / 255.0
        r = (col >> 16 & 0xFF) / 255.0
        g = (col >> 8 & 0xFF) / 255.0
        b = (col & 0xFF) / 255.0
        t = tesselator
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glColor4f(r, g, b, a)
        t.begin()
        t.vertex(x0, y1, 0.0)
        t.vertex(x1, y1, 0.0)
        t.vertex(x1, y0, 0.0)
        t.vertex(x0, y0, 0.0)
        t.end()
        gl.glDisable(gl.GL_BLEND)

    def _fillGradient(self, x0, y0, x1, y1, col1, col2):
        a1 = (col1 >> 24 & 0xFF) / 255.0
        r1 = (col1 >> 16 & 0xFF) / 255.0
        g1 = (col1 >> 8 & 0xFF) / 255.0
        b1 = (col1 & 0xFF) / 255.0

        a2 = (col2 >> 24 & 0xFF) / 255.0
        r2 = (col2 >> 16 & 0xFF) / 255.0
        g2 = (col2 >> 8 & 0xFF) / 255.0
        b2 = (col2 & 0xFF) / 255.0
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glBegin(gl.GL_QUADS)
        gl.glColor4f(r1, g1, b1, a1)
        gl.glVertex2f(x1, y0)
        gl.glVertex2f(x0, y0)
        gl.glColor4f(r2, g2, b2, a2)
        gl.glVertex2f(x0, y1)
        gl.glVertex2f(x1, y1)
        gl.glEnd()
        gl.glDisable(gl.GL_BLEND)

    def drawCenteredString(self, string, x, y, color):
        self.minecraft.font.drawShadow(string, x - self.minecraft.font.width(string) // 2, y, color)

    def drawString(self, string, x, y, color):
        self.minecraft.font.drawShadow(string, x, y, color)

    def updateEvents(self, button=None, key=None):
        if button:
            xm = self.minecraft.mouseX * self.width // self.minecraft.width
            ym = self.height - self.minecraft.mouseY * self.height // self.minecraft.height - 1
            self._mouseClicked(xm, ym, button)
        if key:
            self._keyPressed(key)

    def _keyPressed(self, key):
        pass

    def _mouseClicked(self, x, y, button):
        pass

    def tick(self):
        pass
