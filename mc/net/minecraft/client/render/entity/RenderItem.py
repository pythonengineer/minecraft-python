from mc.net.minecraft.client.render.Tessellator import tessellator
from mc.net.minecraft.client.render.entity.Render import Render
from mc.net.minecraft.client.render.RenderBlocks import RenderBlocks
from mc.net.minecraft.game.level.block.Blocks import blocks
from mc.JavaUtils import Random
from pyglet import gl

import math

class RenderItem(Render):

    def __init__(self):
        super().__init__()
        self.__renderBlocks = RenderBlocks(tessellator)
        self.__random = Random()

    def doRender(self, entity, xd, yd, zd, yaw, a):
        self.__random.setSeed(187)
        item = entity.item
        gl.glPushMatrix()
        hoverY = math.sin((entity.age + a) / 10.0 + entity.hoverStart) * 0.1 + 0.1
        rot = ((entity.age + a) / 20.0 + entity.hoverStart) * (180.0 / math.pi)
        renders = 1
        if entity.item.stackSize > 1:
            renders = 2
        if entity.item.stackSize > 5:
            renders = 3
        if entity.item.stackSize > 20:
            renders = 4

        gl.glTranslatef(xd, yd + hoverY, zd)
        gl.glEnable(gl.GL_NORMALIZE)
        if item.itemID < 256:
            gl.glRotatef(rot, 0.0, 1.0, 0.0)
            self._loadTexture('terrain.png')
            scale = 0.25
            if not blocks.blocksList[item.itemID].renderAsNormalBlock() and \
               item.itemID != blocks.stairSingle.blockID:
                scale = 0.5

            gl.glScalef(scale, scale, scale)

            for i in range(renders):
                gl.glPushMatrix()
                if i > 0:
                    x = (self.__random.nextFloat() * 2.0 - 1.0) * 0.2 / scale
                    y = (self.__random.nextFloat() * 2.0 - 1.0) * 0.2 / scale
                    z = (self.__random.nextFloat() * 2.0 - 1.0) * 0.2 / scale
                    gl.glTranslatef(x, y, z)

                self.__renderBlocks.renderBlockOnInventory(blocks.blocksList[item.itemID])
                gl.glPopMatrix()
        else:
            gl.glScalef(0.5, 0.5, 0.5)
            self._loadTexture('gui/items.png')
            t = tessellator
            iconIndex = item.getItem().getIconIndex()
            u0 = (iconIndex % 16 << 4) / 256.0
            u1 = ((iconIndex % 16 << 4) + 16) / 256.0
            v0 = (iconIndex // 16 << 4) / 256.0
            v1 = ((iconIndex // 16 << 4) + 16) / 256.0

            for i in range(renders):
                gl.glPushMatrix()
                if i > 0:
                    x = (self.__random.nextFloat() * 2.0 - 1.0) * 0.3
                    y = (self.__random.nextFloat() * 2.0 - 1.0) * 0.3
                    z = (self.__random.nextFloat() * 2.0 - 1.0) * 0.3
                    gl.glTranslatef(x, y, z)

                gl.glRotatef(-self._renderManager.playerViewY, 0.0, 1.0, 0.0)
                t.startDrawingQuads()
                t.setNormal(0.0, 1.0, 0.0)
                t.addVertexWithUV(-0.5, -0.25, 0.0, u0, v1)
                t.addVertexWithUV(0.5, -0.25, 0.0, u1, v1)
                t.addVertexWithUV(0.5, 12.0 / 16.0, 0.0, u1, v0)
                t.addVertexWithUV(-0.5, 12.0 / 16.0, 0.0, u0, v0)
                t.draw()
                gl.glPopMatrix()

        gl.glDisable(gl.GL_NORMALIZE)
        gl.glPopMatrix()
