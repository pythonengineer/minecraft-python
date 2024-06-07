from mc.net.minecraft.client.render.Tessellator import tessellator
from mc.net.minecraft.client.render.entity.Render import Render
from pyglet import gl

class RenderEntity(Render):

    def doRender(self, entity, xd, yd, zd, yaw, a):
        gl.glPushMatrix()
        gl.glTranslatef(xd - entity.lastTickPosX, yd - entity.lastTickPosY,
                        zd - entity.lastTickPosZ)
        Render.renderOffsetAABB(entity.boundingBox)
        gl.glPopMatrix()
