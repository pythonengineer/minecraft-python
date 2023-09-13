from mc.net.minecraft.renderer.Tesselator import tesselator
from mc.net.minecraft.level.tile.Tiles import tiles
from mc.net.minecraft.gui.Screen import Screen
from mc.net.minecraft.User import User
from pyglet import window, gl

class BlockSelectionScreen(Screen):

    def __init__(self):
        self.allowUserInput = True

    def __getTiles(self, x, y):
        for i in range(len(User.creativeTiles)):
            w = self._width // 2 + i % 9 * 24 + -108 - 3
            h = self._height // 2 + i // 9 * 24 + -60 + 3
            if x >= w and x <= w + 24 and y >= h - 12 and y <= h + 12:
                return i

        return -1

    def render(self, xm, ym):
        xm = self.__getTiles(xm, ym)
        self._fillGradient(self._width // 2 - 120, 30, self._width // 2 + 120, 180, -1878719232, -1070583712)
        if xm >= 0:
            w = self._width // 2 + xm % 9 * 24 + -108
            h = self._height // 2 + xm // 9 * 24 + -60
            self._fillGradient(w - 3, h - 8, w + 23, h + 24 - 6, -1862270977, -1056964609)

        self.drawCenteredString(self._font, 'Select block', self._width // 2, 40, 0xFFFFFF)
        t = tesselator
        tex = self._minecraft.textures.loadTexture('terrain.png')
        gl.glBindTexture(gl.GL_TEXTURE_2D, tex)

        for i in range(len(User.creativeTiles)):
            tile = User.creativeTiles[i]
            gl.glPushMatrix()
            w = self._width // 2 + i % 9 * 24 + -108
            h = self._height // 2 + i // 9 * 24 + -60
            gl.glTranslatef(w, h, 0.0)
            gl.glScalef(10.0, 10.0, 10.0)
            gl.glTranslatef(1.0, 0.5, 8.0)
            gl.glRotatef(-30.0, 1.0, 0.0, 0.0)
            gl.glRotatef(45.0, 0.0, 1.0, 0.0)
            if xm == i:
                gl.glScalef(1.6, 1.6, 1.6)

            gl.glTranslatef(-1.5, 0.5, 0.5)
            gl.glScalef(-1.0, -1.0, -1.0)
            t.begin()
            tile.render(t)
            t.end()
            gl.glPopMatrix()

    def _mouseClicked(self, xm, ym, button):
        if button == window.mouse.LEFT:
            self._minecraft.player.inventory.replaceSlot(self.__getTiles(xm, ym))
            self._minecraft.setScreen(None)
