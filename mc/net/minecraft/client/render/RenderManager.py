from mc.net.minecraft.client.model.ModelBiped import ModelBiped
from mc.net.minecraft.client.model.md3.MD3Loader import MD3Loader
from mc.net.minecraft.client.model.md3.MD3Model import MD3Model
from mc.net.minecraft.client.render.Tessellator import tessellator
from mc.net.minecraft.client.render.RenderBlocks import RenderBlocks
from mc.net.minecraft.game.entity.EntityLiving import EntityLiving
from mc.net.minecraft.game.entity.misc.EntityItem import EntityItem
from mc.net.minecraft.game.entity.misc.EntityTNTPrimed import EntityTNTPrimed
from mc.net.minecraft.game.level.block.Blocks import blocks
from pyglet import gl

class RenderManager:

    def __init__(self):
        ModelBiped()
        self.__model = [None]
        self.worldObj = None
        self.__blockRenderer = RenderBlocks(tessellator)
        self.playerViewY = 0.0

        try:
            self.__model[0] = MD3Model((MD3Loader()).loadModel('test2.md3'))
        except IOError as e:
            print(e)

    def renderEntityWithPosYaw(self, entity, renderEngine, xd, yd, zd, yaw, a):
        if not isinstance(entity, EntityLiving):
            if isinstance(entity, EntityTNTPrimed):
                gl.glPushMatrix()
                gl.glTranslatef(xd, yd, zd)
                tex = renderEngine.getTexture('terrain.png')
                gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
                self.__blockRenderer.renderBlockOnInventory(blocks.tnt)
                gl.glPopMatrix()
            elif isinstance(entity, EntityItem):
                gl.glPushMatrix()
                gl.glTranslatef(xd, yd, zd)
                gl.glEnable(gl.GL_NORMALIZE)
                if entity.item.itemID > 0:
                    gl.glPushMatrix()
                    gl.glScalef(0.25, 0.25, 0.25)
                    tex = renderEngine.getTexture('terrain.png')
                    gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
                    self.__blockRenderer.renderBlockOnInventory(blocks.blocksList[entity.item.itemID])
                    gl.glPopMatrix()
                else:
                    gl.glScalef(0.5, 0.5, 0.5)
                    tex = renderEngine.getTexture('gui/items.png')
                    gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
                    t = tessellator
                    iconIndex = entity.item.iconIndex
                    u0 = (iconIndex % 16 << 4) / 256.0
                    u1 = ((iconIndex % 16 << 4) + 16) / 256.0
                    v0 = (iconIndex // 16 << 4) / 256.0
                    v1 = ((iconIndex // 16 << 4) + 16) / 256.0
                    gl.glRotatef(-self.playerViewY, 0.0, 1.0, 0.0)
                    t.startDrawingQuads()
                    tessellator.setNormal(0.0, 1.0, 0.0)
                    t.addVertexWithUV(0.0 - 0.5, 0.0 - 0.25, 0.0, u0, v1)
                    t.addVertexWithUV(1.0 - 0.5, 0.0 - 0.25, 0.0, u1, v1)
                    t.addVertexWithUV(1.0 - 0.5, 1.0 - 0.25, 0.0, u1, v0)
                    t.addVertexWithUV(0.0 - 0.5, 1.0 - 0.25, 0.0, u0, v0)
                    t.draw()
                    t.draw()

                gl.glDisable(gl.GL_NORMALIZE)
                gl.glPopMatrix()
        else:
            gl.glEnable(gl.GL_BLEND)
            renderEngine.clampTexture = True
            tex = renderEngine.getTexture('shadow.png')
            gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
            renderEngine.clampTexture = False
            gl.glDepthMask(False)
            ofs = 0.5

            for xx in range(int(xd - ofs), int(xd + ofs + 1)):
                for yy in range(int(yd - 2.0), int(yd + 1)):
                    for zz in range(int(zd - ofs), int(zd + ofs + 1)):
                        blockId = self.worldObj.getBlockId(xx, yy - 1, zz)
                        if blockId > 0 and self.worldObj.isHalfLit(xx, yy, zz):
                            block = blocks.blocksList[blockId]
                            t = tessellator
                            r0 = (1.0 - (yd - yy) / 2.0) * 0.5
                            if r0 >= 0.0:
                                gl.glColor4f(1.0, 1.0, 1.0, r0)
                                t.startDrawingQuads()
                                r0 = xx + block.minX
                                r1 = xx + block.maxX
                                g = yy + block.minY
                                b0 = zz + block.minZ
                                b1 = zz + block.maxZ
                                u0 = (xd - r0) / 2.0 / ofs + 0.5
                                u1 = (xd - r1) / 2.0 / ofs + 0.5
                                v0 = (zd - b0) / 2.0 / ofs + 0.5
                                v1 = (zd - b1) / 2.0 / ofs + 0.5
                                t.addVertexWithUV(r0, g, b0, u0, v0)
                                t.addVertexWithUV(r0, g, b1, u0, v1)
                                t.addVertexWithUV(r1, g, b1, u1, v1)
                                t.addVertexWithUV(r1, g, b0, u1, v0)
                                t.draw()

            gl.glColor4f(1.0, 1.0, 1.0, 1.0)
            gl.glDisable(gl.GL_BLEND)
            gl.glDepthMask(True)
            gl.glPushMatrix()

            try:
                zo = entity.prevRenderYawOffset + (entity.renderYawOffset - entity.prevRenderYawOffset) * a
                zo *= yaw
                gl.glTranslatef(xd, yd, zd)
                tex = renderEngine.getTexture('cube-nes.png')
                gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
                gl.glRotatef(-zo + 180.0, 0.0, 1.0, 0.0)
                gl.glRotatef(-90.0, 1.0, 0.0, 0.0)
                gl.glScalef(0.02, -0.02, 0.02)
                gl.glEnable(gl.GL_NORMALIZE)
                self.__model[0].renderModelVertices()
                gl.glDisable(gl.GL_NORMALIZE)
            except Exception as e:
                print(e)

            gl.glPopMatrix()
