from mc.net.minecraft.client.render.Tessellator import tessellator
from mc.net.minecraft.client.render.entity.Render import Render
from pyglet import gl

class RenderEntity(Render):

    def doRender(self, entity, xd, yd, zd, yaw, a):
        gl.glPushMatrix()
        gl.glTranslatef(xd - entity.lastTickPosX, yd - entity.lastTickPosY,
                        zd - entity.lastTickPosZ)
        bb = entity.boundingBox
        gl.glDisable(gl.GL_TEXTURE_2D)
        t = tessellator
        gl.glColor4(1.0, 1.0, 1.0, 1.0)
        t.startDrawingQuads()
        t.setNormal(0.0, 0.0, -1.0)
        t.addVertex(bb.minX, bb.maxY, bb.minZ)
        t.addVertex(bb.maxX, bb.maxY, bb.minZ)
        t.addVertex(bb.maxX, bb.minY, bb.minZ)
        t.addVertex(bb.minX, bb.minY, bb.minZ)
        t.setNormal(0.0, 0.0, 1.0)
        t.addVertex(bb.minX, bb.minY, bb.maxZ)
        t.addVertex(bb.maxX, bb.minY, bb.maxZ)
        t.addVertex(bb.maxX, bb.maxY, bb.maxZ)
        t.addVertex(bb.minX, bb.maxY, bb.maxZ)
        t.setNormal(0.0, -1.0, 0.0)
        t.addVertex(bb.minX, bb.minY, bb.minZ)
        t.addVertex(bb.maxX, bb.minY, bb.minZ)
        t.addVertex(bb.maxX, bb.minY, bb.maxZ)
        t.addVertex(bb.minX, bb.minY, bb.maxZ)
        t.setNormal(0.0, 1.0, 0.0)
        t.addVertex(bb.minX, bb.maxY, bb.maxZ)
        t.addVertex(bb.maxX, bb.maxY, bb.maxZ)
        t.addVertex(bb.maxX, bb.maxY, bb.minZ)
        t.addVertex(bb.minX, bb.maxY, bb.minZ)
        t.setNormal(-1.0, 0.0, 0.0)
        t.addVertex(bb.minX, bb.minY, bb.maxZ)
        t.addVertex(bb.minX, bb.maxY, bb.maxZ)
        t.addVertex(bb.minX, bb.maxY, bb.minZ)
        t.addVertex(bb.minX, bb.minY, bb.minZ)
        t.setNormal(1.0, 0.0, 0.0)
        t.addVertex(bb.maxX, bb.minY, bb.minZ)
        t.addVertex(bb.maxX, bb.maxY, bb.minZ)
        t.addVertex(bb.maxX, bb.maxY, bb.maxZ)
        t.addVertex(bb.maxX, bb.minY, bb.maxZ)
        t.draw()
        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glPopMatrix()
