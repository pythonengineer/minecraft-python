from mc.net.minecraft.client.model.ModelBiped import ModelBiped
from mc.net.minecraft.client.render.Tessellator import tessellator
from mc.net.minecraft.client.render.RenderBlocks import RenderBlocks
from mc.net.minecraft.game.level.block.Blocks import blocks
from pyglet import gl

class Render:

    def __init__(self):
        ModelBiped()
        RenderBlocks(tessellator)
        self._renderManager = None
        self._shadowSize = 0.0

    def doRender(self, entity, xd, yd, zd, yaw, a):
        pass

    def _loadTexture(self, tex):
        gl.glBindTexture(gl.GL_TEXTURE_2D,
                         self._renderManager.renderEngine.getTexture(tex))

    def setRenderManager(self, renderManager):
        self._renderManager = renderManager

    def renderShadow(self, entity, xd, yd, zd, a):
        if self._shadowSize > 0.0:
            gl.glEnable(gl.GL_BLEND)
            self._renderManager.renderEngine.setClampTexture(True)
            tex = self._renderManager.renderEngine.getTexture('shadow.png')
            gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
            self._renderManager.renderEngine.setClampTexture(False)
            gl.glDepthMask(False)

            for xx in range(int(xd - self._shadowSize), int(xd + self._shadowSize + 1)):
                for yy in range(int(yd - 2.0), int(yd + 1)):
                    for zz in range(int(zd - self._shadowSize), int(zd + self._shadowSize + 1)):
                        blockId = self._renderManager.worldObj.getBlockId(xx, yy - 1, zz)
                        if blockId > 0 and self._renderManager.worldObj.isHalfLit(xx, yy, zz):
                            block = blocks.blocksList[blockId]
                            t = tessellator
                            br = self._renderManager.worldObj.getBlockLightValue(xx, yy, zz)
                            r0 = (1.0 - (yd - yy) / 2.0) * 0.5 * br
                            if r0 >= 0.0:
                                gl.glColor4f(1.0, 1.0, 1.0, r0)
                                t.startDrawingQuads()
                                r0 = xx + block.minX
                                r1 = xx + block.maxX
                                g = yy + block.minY
                                b0 = zz + block.minZ
                                b1 = zz + block.maxZ
                                u0 = (xd - r0) / 2.0 / 0.5 + 0.5
                                u1 = (xd - r1) / 2.0 / 0.5 + 0.5
                                v0 = (zd - b0) / 2.0 / 0.5 + 0.5
                                v1 = (zd - b1) / 2.0 / 0.5 + 0.5
                                t.addVertexWithUV(r0, g, b0, u0, v0)
                                t.addVertexWithUV(r0, g, b1, u0, v1)
                                t.addVertexWithUV(r1, g, b1, u1, v1)
                                t.addVertexWithUV(r1, g, b0, u1, v0)
                                t.draw()

            gl.glColor4f(1.0, 1.0, 1.0, 1.0)
            gl.glDisable(gl.GL_BLEND)
            gl.glDepthMask(True)

        if entity.fire > 0:
            gl.glDisable(gl.GL_LIGHTING)
            tex = blocks.fire.blockIndexInTexture
            xt = (tex & 15) << 4
            tex &= 240
            u0 = xt / 256.0
            u1 = (xt + 15.99) / 256.0
            v0 = tex / 256.0
            v1 = (tex + 15.99) / 256.0
            gl.glPushMatrix()
            gl.glTranslatef(xd, yd, zd)
            scale = entity.width * 1.4
            gl.glScalef(scale, scale, scale)
            self._loadTexture('terrain.png')
            t = tessellator
            xo = 1.0
            zo = 0.0
            aspect = entity.height / entity.width
            gl.glRotatef(-self._renderManager.playerViewY, 0.0, 1.0, 0.0)
            gl.glTranslatef(0.0, 0.0, 0.4 + int(aspect) * 0.02)
            gl.glColor4f(1.0, 1.0, 1.0, 1.0)
            t.startDrawingQuads()

            while aspect > 0.0:
                t.addVertexWithUV(-0.5, 0.0 - zo, 0.0, u0, v1)
                t.addVertexWithUV(xo - 0.5, 0.0 - zo, 0.0, u1, v1)
                t.addVertexWithUV(xo - 0.5, 1.4 - zo, 0.0, u1, v0)
                t.addVertexWithUV(-0.5, 1.4 - zo, 0.0, u0, v0)
                aspect -= 1.0
                zo -= 1.0
                xo *= 0.9
                gl.glTranslatef(0.0, 0.0, -0.04)

            t.draw()
            gl.glPopMatrix()
            gl.glEnable(gl.GL_LIGHTING)
