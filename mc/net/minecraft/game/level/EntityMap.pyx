# cython: language_level=3
# cython: cdivision=True

from mc.net.minecraft.game.entity.Entity cimport Entity
from mc.net.minecraft.game.entity.EntityLiving import EntityLiving
from mc.net.minecraft.game.level.EntityMapSlot cimport EntityMapSlot
from mc.net.minecraft.game.physics.AxisAlignedBB cimport AxisAlignedBB
from mc.net.minecraft.game.level.block.Blocks import blocks
from mc.net.minecraft.client.player.EntityPlayer import EntityPlayer
from mc.net.minecraft.client.render.ClippingHelper cimport ClippingHelper
from mc.net.minecraft.client.render.Tessellator cimport Tessellator
from mc.net.minecraft.client.render.Tessellator import tessellator

from pyglet import gl

cdef class EntityMap:

    def __init__(self, int w, int h, int d):
        self.slot0 = EntityMapSlot(self)
        self.slot1 = EntityMapSlot(self)
        self.entities = []
        self.__entitiesExcludingEntity = []
        self.xSlot = w // 16
        self.ySlot = h // 16
        self.zSlot = d // 16
        if self.xSlot == 0:
            self.xSlot = 1
        if self.ySlot == 0:
            self.ySlot = 1
        if self.zSlot == 0:
            self.zSlot = 1

        self.entityGrid = [None] * self.xSlot * self.ySlot * self.zSlot
        for w in range(self.xSlot):
            for h in range(self.ySlot):
                for d in range(self.zSlot):
                    self.entityGrid[(d * self.ySlot + h) * self.xSlot + w] = []

    cpdef list getEntitiesWithinAABBExcludingEntity(self, Entity oEntity, AxisAlignedBB aabb):
        cdef float x0, y0, z0, x1, y1, z1
        cdef int x, y, z
        cdef Entity entity

        self.__entitiesExcludingEntity.clear()
        x0 = aabb.x0
        y0 = aabb.y0
        z0 = aabb.z0
        x1 = aabb.x1
        y1 = aabb.y1
        z1 = aabb.z1

        slot = self.slot0.init(x0, y0, z0)
        slot2 = self.slot1.init(x1, y1, z1)

        for x in range(slot.xSlot - 1, slot2.xSlot + 2):
            for y in range(slot.ySlot - 1, slot2.ySlot + 2):
                for z in range(slot.zSlot - 1, slot2.zSlot + 2):
                    if x >= 0 and y >= 0 and z >= 0 and x < self.xSlot and y < self.ySlot and z < self.zSlot:
                        entities = self.entityGrid[(z * self.ySlot + y) * self.xSlot + x]
                        for entity in entities:
                            if entity != oEntity and entity.boundingBox.intersects(x0, y0, z0,
                                                                                   x1, y1, z1):
                                self.__entitiesExcludingEntity.append(entity)

        return self.__entitiesExcludingEntity

    cdef tickAll(self):
        cdef int xOld, yOld, zOld, x, y, z
        cdef Entity entity
        cdef EntityMapSlot oldSlot, newSlot

        for entity in list(self.entities):
            entity.lastTickPosX = entity.posX
            entity.lastTickPosY = entity.posY
            entity.lastTickPosZ = entity.posZ
            entity.onEntityUpdate()
            entity.ticksExisted += 1
            if entity.isDead:
                try:
                    self.entities.remove(entity)
                except:
                    pass

                self.slot0.init(entity.lastTickPosX,
                                entity.lastTickPosY,
                                entity.lastTickPosZ).remove(entity)
                continue

            xOld = <int>(entity.lastTickPosX // 16.0)
            yOld = <int>(entity.lastTickPosY // 16.0)
            zOld = <int>(entity.lastTickPosZ // 16.0)
            x = <int>(entity.posX // 16.0)
            y = <int>(entity.posY // 16.0)
            z = <int>(entity.posZ // 16.0)
            if xOld != x or yOld != y or zOld != z:
                oldSlot = self.slot0.init(entity.lastTickPosX, entity.lastTickPosY,
                                          entity.lastTickPosZ)
                newSlot = self.slot1.init(entity.posX, entity.posY, entity.posZ)
                if oldSlot != newSlot:
                    oldSlot.remove(entity)
                    newSlot.add(entity)

    cpdef render(self, vec, ClippingHelper clippingHelper, renderManager, renderEngine, float a):
        cdef int x, y, z, xx, yy, zz, tex, blockId
        cdef float x0, x1, y0, y1, z0, z1, xd, yd, zd, ofs, r0, r1, g, b0, b1
        cdef float u0, u1, v0, v1, zo, br
        cdef bint li, exists
        cdef Entity entity
        cdef Tessellator t

        for x in range(self.xSlot):
            x0 = (x << 4) - 2
            x1 = (x + 1 << 4) + 2
            for y in range(self.ySlot):
                y0 = (y << 4) - 2
                y1 = (y + 1 << 4) + 2
                for z in range(self.zSlot):
                    entities = self.entityGrid[(z * self.ySlot + y) * self.xSlot + x]
                    if not entities:
                        continue

                    z0 = (z << 4) - 2
                    z1 = (z + 1 << 4) + 2
                    if clippingHelper.isBoundingBoxInFrustrum(x0, y0, z0, x1, y1, z1):
                        exists = clippingHelper.isBoundingBoxFullyInFrustrum(x0, y0, z0,
                                                                             x1, y1, z1)
                        for entity in entities:
                            if entity.shouldRender(vec) and (exists or clippingHelper.isVisible(entity.boundingBox)):
                                if isinstance(entity, EntityPlayer):
                                    continue

                                xd = entity.lastTickPosX + (entity.posX - entity.lastTickPosX) * a
                                yd = entity.lastTickPosY + (entity.posY - entity.lastTickPosY) * a
                                zd = entity.lastTickPosZ + (entity.posZ - entity.lastTickPosZ) * a
                                gl.glEnable(gl.GL_BLEND)
                                renderEngine.clampTexture = True
                                tex = renderEngine.getTexture('shadow.png')
                                gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
                                renderEngine.clampTexture = False
                                #gl.glDepthMask(False)
                                ofs = 0.5

                                for xx in range(<int>(xd - ofs), <int>(xd + ofs + 1)):
                                    for yy in range(<int>(yd - 2.0), <int>(yd + 1)):
                                        for zz in range(<int>(zd - ofs), <int>(zd + ofs + 1)):
                                            blockId = renderManager.worldObj.getBlockId(xx, yy - 1, zz)
                                            if blockId > 0 and renderManager.worldObj.isHalfLit(xx, yy, zz):
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
                                                    t.addVertexWithUV(r0, g + 0.01, b0, u0, v0)
                                                    t.addVertexWithUV(r0, g + 0.01, b1, u0, v1)
                                                    t.addVertexWithUV(r1, g + 0.01, b1, u1, v1)
                                                    t.addVertexWithUV(r1, g + 0.01, b0, u1, v0)
                                                    t.draw()

                                gl.glColor4f(1.0, 1.0, 1.0, 1.0)
                                gl.glDisable(gl.GL_BLEND)
                                #gl.glDepthMask(True)
                                if isinstance(entity, EntityLiving):
                                    gl.glPushMatrix()

                                    try:
                                        zo = entity.prevRenderYawOffset + (entity.renderYawOffset - entity.prevRenderYawOffset) * z0
                                        gl.glTranslatef(xd, yd, zd)
                                        tex = renderEngine.getTexture('cube-nes.png')
                                        gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
                                        gl.glRotatef(-zo + 180.0, 0.0, 1.0, 0.0)
                                        br = renderManager.worldObj.getBlockLightValue(xd, yd, zd)
                                        gl.glColor3f(br, br, br)
                                        gl.glRotatef(-90.0, 1.0, 0.0, 0.0)
                                        gl.glScalef(0.02, -0.02, 0.02)
                                        gl.glEnable(gl.GL_NORMALIZE)
                                        renderManager.model[0].renderModelVertices(0, 0, 0.0)
                                        gl.glDisable(gl.GL_NORMALIZE)
                                    except Exception as e:
                                        print(e)

                                    gl.glPopMatrix()
                                else:
                                    bb = entity.boundingBox
                                    gl.glDisable(gl.GL_TEXTURE_2D)
                                    t = tessellator
                                    gl.glColor4f(1.0, 1.0, 1.0, 1.0)
                                    t.startDrawingQuads()
                                    Tessellator.setNormal(0.0, 0.0, -1.0)
                                    t.addVertex(bb.x0, bb.y1, bb.z0)
                                    t.addVertex(bb.x1, bb.y1, bb.z0)
                                    t.addVertex(bb.x1, bb.y0, bb.z0)
                                    t.addVertex(bb.x0, bb.y0, bb.z0)
                                    Tessellator.setNormal(0.0, 0.0, 1.0)
                                    t.addVertex(bb.x0, bb.y0, bb.z1)
                                    t.addVertex(bb.x1, bb.y0, bb.z1)
                                    t.addVertex(bb.x1, bb.y1, bb.z1)
                                    t.addVertex(bb.x0, bb.y1, bb.z1)
                                    Tessellator.setNormal(0.0, -1.0, 0.0)
                                    t.addVertex(bb.x0, bb.y0, bb.z0)
                                    t.addVertex(bb.x1, bb.y0, bb.z0)
                                    t.addVertex(bb.x1, bb.y0, bb.z1)
                                    t.addVertex(bb.x0, bb.y0, bb.z1)
                                    Tessellator.setNormal(0.0, 1.0, 0.0)
                                    t.addVertex(bb.x0, bb.y1, bb.z1)
                                    t.addVertex(bb.x1, bb.y1, bb.z1)
                                    t.addVertex(bb.x1, bb.y1, bb.z0)
                                    t.addVertex(bb.x0, bb.y1, bb.z0)
                                    Tessellator.setNormal(-1.0, 0.0, 0.0)
                                    t.addVertex(bb.x0, bb.y0, bb.z1)
                                    t.addVertex(bb.x0, bb.y1, bb.z1)
                                    t.addVertex(bb.x0, bb.y1, bb.z0)
                                    t.addVertex(bb.x0, bb.y0, bb.z0)
                                    Tessellator.setNormal(1.0, 0.0, 0.0)
                                    t.addVertex(bb.x1, bb.y0, bb.z0)
                                    t.addVertex(bb.x1, bb.y1, bb.z0)
                                    t.addVertex(bb.x1, bb.y1, bb.z1)
                                    t.addVertex(bb.x1, bb.y0, bb.z1)
                                    t.draw()
                                    gl.glEnable(gl.GL_TEXTURE_2D)
                                    gl.glPushMatrix()
                                    gl.glTranslatef(xd, yd, zd)
                                    yd = 0.02
                                    gl.glRotatef(-90.0, 1.0, 0.0, 0.0)
                                    gl.glScalef(yd, -yd, yd)
                                    renderManager.model[0].renderModelVertices(0, 0, a)
                                    gl.glPopMatrix()
