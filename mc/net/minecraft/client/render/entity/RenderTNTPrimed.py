from mc.net.minecraft.client.render.Tessellator import tessellator
from mc.net.minecraft.client.render.entity.Render import Render
from mc.net.minecraft.client.render.RenderBlocks import RenderBlocks
from mc.net.minecraft.game.level.block.Blocks import blocks
from pyglet import gl

class RenderTNTPrimed(Render):
    __blockRenderer = RenderBlocks(tessellator)

    def __init__(self):
        super().__init__()
        self._shadowSize = 0.5

    def doRender(self, entity, xd, yd, zd, yaw, a):
        gl.glPushMatrix()
        gl.glTranslatef(xd, yd, zd)
        if entity.fuse - a + 1.0 < 10.0:
            scale = 1.0 - (entity.fuse - a + 1.0) / 10.0
            scale = min(max(scale, 0.0), 1.0)
            scale *= scale
            scale *= scale
            scale = 1.0 + scale * 0.3
            gl.glScalef(scale, scale, scale)

        alpha = (1.0 - (entity.fuse - a + 1.0) / 100.0) * 0.8

        self._loadTexture('terrain.png')
        self.__blockRenderer.renderBlockOnInventory(blocks.tnt)
        if entity.fuse // 5 % 2 == 0:
            gl.glDisable(gl.GL_TEXTURE_2D)
            gl.glDisable(gl.GL_LIGHTING)
            gl.glEnable(gl.GL_BLEND)
            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_DST_ALPHA)
            gl.glColor4f(1.0, 1.0, 1.0, alpha)
            self.__blockRenderer.renderBlockOnInventory(blocks.tnt)
            gl.glColor4f(1.0, 1.0, 1.0, 1.0)
            gl.glDisable(gl.GL_BLEND)
            gl.glEnable(gl.GL_LIGHTING)
            gl.glEnable(gl.GL_TEXTURE_2D)

        gl.glPopMatrix()
