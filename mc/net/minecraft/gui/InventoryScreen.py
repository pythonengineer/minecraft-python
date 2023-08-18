from mc.net.minecraft.renderer.Tesselator import tesselator
from mc.net.minecraft.gui.Screen import Screen
from mc.net.minecraft.User import User
from pyglet import window, gl

class InventoryScreen(Screen):

    def __getTileAtSlot(self, xm, ym):
        for i in range(len(User.creativeTiles)):
            i4 = self._width // 2 + i % 8 * 24 - 96
            i5 = self._height // 2 + i // 8 * 24 - 48
            if xm >= i4 and xm <= i4 + 24 and ym >= i5 - 12 and ym <= i5 + 12:
                return i

        return -1

    def render(self, xm, ym):
        self._fillGradient(0, 0, self._width, self._height, 1610941696, -1607454624)
        self.drawCenteredString('Select block', self._width // 2, 40, 0xFFFFFF)
        t = tesselator
        tileAtSlot = self.__getTileAtSlot(xm, ym)
        id_ = self._minecraft.textures.getTextureId('terrain.png')
        gl.glBindTexture(gl.GL_TEXTURE_2D, id_)
        gl.glEnable(gl.GL_TEXTURE_2D)

        for i in range(len(User.creativeTiles)):
            tile = User.creativeTiles[i]
            gl.glPushMatrix()
            i5 = self._width // 2 + i % 8 * 24 - 96
            i6 = self._height // 2 + i // 8 * 24 - 48
            gl.glTranslatef(i5, i6, 0.0)
            gl.glScalef(10.0, 10.0, 10.0)
            gl.glTranslatef(1.0, 0.5, 8.0)
            gl.glRotatef(-30.0, 1.0, 0.0, 0.0)
            gl.glRotatef(45.0, 0.0, 1.0, 0.0)
            if tileAtSlot == i:
                gl.glScalef(1.6, 1.6, 1.6)

            gl.glTranslatef(-1.5, 0.5, 0.5)
            gl.glScalef(-1.0, -1.0, -1.0)
            t.begin()
            tile.render(t, self._minecraft.level, 0, -2, 0, 0)
            t.end()
            gl.glPopMatrix()

        gl.glDisable(gl.GL_TEXTURE_2D)

    def _mousePressed(self, xm, ym, button):
        if button == window.mouse.LEFT:
            tile = self.__getTileAtSlot(xm, ym)
            if tile >= 0:
                self._minecraft.player.inventory.getSlotContainsTile(User.creativeTiles[tile])

            self._minecraft.setScreen(None)
