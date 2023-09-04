# cython: language_level=3

cimport cython

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

    cdef list getEntities(self, oEntity, float x0, float y0, float z0,
                          float x1, float y1, float z1, list l):
        cdef int x, y, z

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

    cpdef list getEntitiesWithinAABBExcludingEntity(self, entity, aabb):
        self.tmp.clear()
        return self.getEntities(entity, aabb.x0, aabb.y0, aabb.z0,
                                aabb.x1, aabb.y1, aabb.z1, self.tmp)

    cpdef render(self, Frustum frustum, textures, float a):
        cdef int x, y, z
        cdef float x0, x1, y0, y1, z0, z1
        cdef bint li, exists

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
                    li = frustum.cubeInFrustum(x0, y0, z0, x1, y1, z1)
                    exists = li and frustum.cubeFullyInFrustum(x0, y0, z0, x1, y1, z1)
                    if not li:
                        continue

                    for entity in entities:
                        if not exists and not frustum.isVisible(entity.bb):
                            continue

                        entity.render(textures, a)
