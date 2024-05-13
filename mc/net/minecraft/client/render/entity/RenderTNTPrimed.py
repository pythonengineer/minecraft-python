from mc.net.minecraft.client.render.Tessellator import tessellator
from mc.net.minecraft.client.render.entity.Render import Render
from mc.net.minecraft.client.render.RenderBlocks import RenderBlocks
from mc.net.minecraft.game.level.block.Blocks import blocks
from pyglet import gl

class RenderTNTPrimed(Render):
    __renderBlocks = RenderBlocks(tessellator)

    def doRender(self, entity, xd, yd, zd, yaw, a):
        gl.glPushMatrix()
        gl.glTranslatef(xd, yd, zd)
        self._loadTexture('terrain.png')
        self.__renderBlocks.renderBlockOnInventory(blocks.tnt)
        gl.glPopMatrix()
