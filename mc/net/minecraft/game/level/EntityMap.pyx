# cython: language_level=3
# cython: cdivision=True

from mc.net.minecraft.game.entity.Entity cimport Entity
from mc.net.minecraft.game.physics.AxisAlignedBB cimport AxisAlignedBB
from mc.net.minecraft.game.level.EntityMapSlot cimport EntityMapSlot
from mc.net.minecraft.game.level.block.Blocks import blocks

from pyglet import gl

cdef class EntityMap:

    def __init__(self, int w, int h, int d):
        self.__slot0 = EntityMapSlot(self)
        self.__slot1 = EntityMapSlot(self)
        self.all = []
        self.__tmp = []
        self.width = w // 16
        self.depth = h // 16
        self.height = d // 16
        if self.width == 0:
            self.width = 1
        if self.depth == 0:
            self.depth = 1
        if self.height == 0:
            self.height = 1

        self.entityGrid = [None] * self.width * self.depth * self.height
        for w in range(self.width):
            for h in range(self.depth):
                for d in range(self.height):
                    self.entityGrid[(d * self.depth + h) * self.width + w] = []

    cdef add(self, Entity entity):
        self.all.append(entity)
        self.__slot0.init(entity.posX, entity.posY, entity.posZ).add(entity)
        entity.lastTickPosX = entity.posX
        entity.lastTickPosY = entity.posY
        entity.lastTickPosZ = entity.posZ

    cdef remove(self, Entity entity):
        self.__slot0.init(entity.lastTickPosX, entity.lastTickPosY, entity.lastTickPosZ).remove(entity)
        try:
            self.all.remove(entity)
        except:
            pass

    cdef list getEntities(self, Entity oEntity, float x0, float y0, float z0,
                          float x1, float y1, float z1):
        self.__tmp.clear()
        return self.__addEntities(oEntity, x0, y0, z0, x1, y1, z1, self.__tmp)

    cdef list __addEntities(self, Entity oEntity, float x0, float y0, float z0,
                            float x1, float y1, float z1, list l):
        cdef int x, y, z
        cdef Entity entity

        slot = self.__slot0.init(x0, y0, z0)
        slot2 = self.__slot1.init(x1, y1, z1)

        for x in range(slot.xSlot - 1, slot2.xSlot + 2):
            for y in range(slot.ySlot - 1, slot2.ySlot + 2):
                for z in range(slot.zSlot - 1, slot2.zSlot + 2):
                    if x >= 0 and y >= 0 and z >= 0 and x < self.width and y < self.depth and z < self.height:
                        entities = self.entityGrid[(z * self.depth + y) * self.width + x]
                        for entity in entities:
                            if entity != oEntity and entity.boundingBox.intersects(x0, y0, z0,
                                                                                   x1, y1, z1):
                                self.__tmp.append(entity)

        return l

    cpdef list getEntitiesWithinAABBExcludingEntity(self, Entity entity, AxisAlignedBB aabb):
        self.__tmp.clear()
        return self.__addEntities(entity, aabb.x0, aabb.y0, aabb.z0,
                                  aabb.x1, aabb.y1, aabb.z1, self.__tmp)

    cdef updateEntities(self):
        cdef int xOld, yOld, zOld, x, y, z
        cdef Entity entity
        cdef EntityMapSlot oldSlot, newSlot

        for entity in list(self.all):
            entity.lastTickPosX = entity.posX
            entity.lastTickPosY = entity.posY
            entity.lastTickPosZ = entity.posZ
            entity.onEntityUpdate()
            entity.ticksExisted += 1
            if entity.isDead:
                try:
                    self.all.remove(entity)
                except:
                    pass

                self.__slot0.init(entity.lastTickPosX,
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
                oldSlot = self.__slot0.init(entity.lastTickPosX, entity.lastTickPosY,
                                            entity.lastTickPosZ)
                newSlot = self.__slot1.init(entity.posX, entity.posY, entity.posZ)
                if oldSlot != newSlot:
                    oldSlot.remove(entity)
                    newSlot.add(entity)
