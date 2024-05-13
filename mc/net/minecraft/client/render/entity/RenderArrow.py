from mc.net.minecraft.client.render.Tessellator import tessellator
from mc.net.minecraft.client.render.entity.Render import Render
from pyglet import gl

import math

class RenderArrow(Render):

    def doRender(self, entity, xd, yd, zd, yaw, a):
        self._loadTexture('item/arrows.png')
        gl.glPushMatrix()
        gl.glTranslatef(xd, yd, zd)
        gl.glRotatef(entity.prevRotationYaw + (entity.rotationYaw - entity.prevRotationYaw) * a - 90.0, 0.0, 1.0, 0.0)
        gl.glRotatef(entity.prevRotationPitch + (entity.rotationPitch - entity.prevRotationPitch) * a, 0.0, 0.0, 1.0)
        t = tessellator
        gl.glEnable(gl.GL_NORMALIZE)
        arrowShake = entity.arrowShake - a
        if arrowShake > 0.0:
            arrowShake = -math.sin(arrowShake * 3.0) * arrowShake
            gl.glRotatef(arrowShake, 0.0, 0.0, 1.0)

        gl.glRotatef(45.0, 1.0, 0.0, 0.0)
        gl.glScalef(0.05625, 0.05625, 0.05625)
        gl.glTranslatef(-4.0, 0.0, 0.0)
        gl.glNormal3f(0.05625, 0.0, 0.0)
        t.startDrawingQuads()
        t.addVertexWithUV(-7.0, -2.0, -2.0, 0.0, 0.15625)
        t.addVertexWithUV(-7.0, -2.0, 2.0, 0.15625, 0.15625)
        t.addVertexWithUV(-7.0, 2.0, 2.0, 0.15625, 5.0 / 16.0)
        t.addVertexWithUV(-7.0, 2.0, -2.0, 0.0, 5.0 / 16.0)
        t.draw()
        gl.glNormal3f(-0.05625, 0.0, 0.0)
        t.startDrawingQuads()
        t.addVertexWithUV(-7.0, 2.0, -2.0, 0.0, 0.15625)
        t.addVertexWithUV(-7.0, 2.0, 2.0, 0.15625, 0.15625)
        t.addVertexWithUV(-7.0, -2.0, 2.0, 0.15625, 5.0 / 16.0)
        t.addVertexWithUV(-7.0, -2.0, -2.0, 0.0, 5.0 / 16.0)
        t.draw()

        for i in range(4):
            gl.glRotatef(90.0, 1.0, 0.0, 0.0)
            gl.glNormal3f(0.0, 0.0, 0.05625)
            t.addVertexWithUV(-8.0, -2.0, 0.0, 0.0, 0.0)
            t.addVertexWithUV(8.0, -2.0, 0.0, 0.5, 0.0)
            t.addVertexWithUV(8.0, 2.0, 0.0, 0.5, 0.15625)
            t.addVertexWithUV(-8.0, 2.0, 0.0, 0.0, 0.15625)
            t.draw()

        gl.glDisable(gl.GL_NORMALIZE)
        gl.glPopMatrix()
