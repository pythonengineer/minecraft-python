# cython: language_level=3
# cython: cdivision=True

from mc.net.minecraft.game.entity.Entity cimport Entity
from mc.net.minecraft.game.entity.EntityLiving import EntityLiving
from mc.net.minecraft.game.entity.player.EntityPlayer import EntityPlayer
from mc.net.minecraft.game.physics.AxisAlignedBB cimport AxisAlignedBB
from mc.net.minecraft.game.level.EntityMapSlot cimport EntityMapSlot
from mc.net.minecraft.game.level.block.Blocks import blocks
from mc.net.minecraft.client.render.ClippingHelper cimport ClippingHelper
from mc.net.minecraft.client.render.Tessellator cimport Tessellator
from mc.net.minecraft.client.render.Tessellator import tessellator

from pyglet import gl

cdef class EntityMap:

    def __init__(self, int w, int h, int d):
        self.slot0 = EntityMapSlot(self)
        self.slot1 = EntityMapSlot(self)
        self.entities = []
        self.entitiesExcludingEntity = []
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

    cdef list getEntities(self, Entity oEntity, float x0, float y0, float z0,
                          float x1, float y1, float z1, list l):
        cdef int x, y, z
        cdef Entity entity

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
                                self.entitiesExcludingEntity.append(entity)

        return self.entitiesExcludingEntity

    cpdef list getEntitiesWithinAABBExcludingEntity(self, Entity entity, AxisAlignedBB aabb):
        self.entitiesExcludingEntity.clear()
        return self.getEntities(entity, aabb.x0, aabb.y0, aabb.z0,
                                aabb.x1, aabb.y1, aabb.z1, self.entitiesExcludingEntity)

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
