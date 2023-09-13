# cython: language_level=3

cimport cython

from mc.net.minecraft.Entity cimport Entity
from mc.net.minecraft.phys.AABB cimport AABB
from mc.net.minecraft.level.Slot cimport Slot
from mc.net.minecraft.renderer.Frustum cimport Frustum

@cython.final
cdef class BlockMap:

    def __init__(self, int w, int d, int h):
        self.slot1 = Slot(self)
        self.slot2 = Slot(self)
        self.all = []
        self.tmp = []
        self.width = w // 16
        self.depth = d // 16
        self.height = h // 16
        if self.width == 0:
            self.width = 1
        if self.depth == 0:
            self.depth = 1
        if self.height == 0:
            self.height = 1

        self.entityGrid = [None] * self.width * self.depth * self.height
        for w in range(self.width):
            for d in range(self.depth):
                for h in range(self.height):
                    self.entityGrid[(h * self.depth + d) * self.width + w] = []

    cdef insert(self, Entity entity):
        self.all.append(entity)
        self.slot1.init(entity.x, entity.y, entity.z).add(entity)
        entity.xOld = entity.x
        entity.yOld = entity.y
        entity.zOld = entity.z
        entity.blockMap = self

    cdef remove(self, Entity entity):
        self.slot1.init(entity.xOld, entity.yOld, entity.zOld).remove(entity)
        try:
            self.all.remove(entity)
        except ValueError:
            pass

    def moved(self, Entity entity):
        cdef Slot oldSlot = self.slot1.init(entity.xOld, entity.yOld, entity.zOld)
        cdef Slot newSlot = self.slot2.init(entity.x, entity.y, entity.z)
        if oldSlot != newSlot:
            oldSlot.remove(entity)
            newSlot.add(entity)
            entity.xOld = entity.x
            entity.yOld = entity.y
            entity.zOld = entity.z

    cdef list getEntities(self, Entity oEntity, float x0, float y0, float z0,
                          float x1, float y1, float z1, list l):
        cdef int x, y, z
        cdef Entity entity

        slot = self.slot1.init(x0, y0, z0)
        slot2 = self.slot2.init(x1, y1, z1)

        for x in range(slot.xSlot - 1, slot2.xSlot + 2):
            for y in range(slot.ySlot - 1, slot2.ySlot + 2):
                for z in range(slot.zSlot - 1, slot2.zSlot + 2):
                    if x >= 0 and y >= 0 and z >= 0 and x < self.width and y < self.depth and z < self.height:
                        entities = self.entityGrid[(z * self.depth + y) * self.width + x]
                        for entity in entities:
                            if entity != oEntity and entity.intersects(x0, y0, z0, x1, y1, z1):
                                l.append(entity)

        return l

    cdef list getEntitiesExcludingEntity(self, Entity entity, float x0, float y0,
                                         float z0, float x1, float y1, float z1):
        self.tmp.clear()
        return self.getEntities(entity, x0, y0, z0, x1, y1, z1, self.tmp)

    cpdef list getEntitiesWithinAABBExcludingEntity(self, Entity entity, AABB aabb):
        self.tmp.clear()
        return self.getEntities(entity, aabb.x0, aabb.y0, aabb.z0,
                                aabb.x1, aabb.y1, aabb.z1, self.tmp)

    cdef list getEntitiesWithinAABBExcludingEntityList(self, Entity entity, AABB aabb, l):
        return self.getEntities(entity, aabb.x0, aabb.y0, aabb.z0,
                                aabb.x1, aabb.y1, aabb.z1, l)

    def removeAllNonCreativeModeEntities(self):
        cdef Entity e

        for w in range(self.width):
            for d in range(self.depth):
                for h in range(self.height):
                    l = self.entityGrid[(h * self.depth + d) * self.width + w]
                    for e in l.copy():
                        if not e.isCreativeModeAllowed():
                            l.remove(e)

    cdef clear(self):
        for w in range(self.width):
            for d in range(self.depth):
                for h in range(self.height):
                    self.entityGrid[(h * self.depth + d) * self.width + w].clear()

    cdef tickAll(self):
        cdef int xOld, yOld, zOld, x, y, z
        cdef Entity entity

        for entity in list(self.all):
            entity.tick()
            if entity.removed:
                self.all.remove(entity)
                self.slot1.init(entity.xOld, entity.yOld, entity.zOld).remove(entity)
                continue

            xOld = <int>(entity.xOld // 16.0)
            yOld = <int>(entity.yOld // 16.0)
            zOld = <int>(entity.zOld // 16.0)
            x = <int>(entity.x // 16.0)
            y = <int>(entity.y // 16.0)
            z = <int>(entity.z // 16.0)
            if xOld != x or yOld != y or zOld != z:
                self.moved(entity)

    cpdef render(self, vec, Frustum frustum, textures, float a):
        cdef int x, y, z
        cdef float x0, x1, y0, y1, z0, z1
        cdef bint li, exists
        cdef Entity entity

        for x in range(self.width):
            x0 = (x << 4) - 2
            x1 = (x + 1 << 4) + 2
            for y in range(self.depth):
                y0 = (y << 4) - 2
                y1 = (y + 1 << 4) + 2
                for z in range(self.height):
                    entities = self.entityGrid[(z * self.depth + y) * self.width + x]
                    if not entities:
                        continue

                    z0 = (z << 4) - 2
                    z1 = (z + 1 << 4) + 2
                    if frustum.cubeInFrustum(x0, y0, z0, x1, y1, z1):
                        exists = frustum.cubeFullyInFrustum(x0, y0, z0, x1, y1, z1)
                        for entity in entities:
                            if entity.shouldRender(vec) and (exists or frustum.isVisible(entity.bb)):
                                entity.render(textures, a)
