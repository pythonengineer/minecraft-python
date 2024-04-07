# cython: language_level=3

cdef class EntityMapSlot:

    def __init__(self, entityMap):
        self.xSlot = 0
        self.ySlot = 0
        self.zSlot = 0
        self.__entityMap = entityMap

    cdef EntityMapSlot init(self, float x, float y, float z):
        self.xSlot = <int>(x // 16)
        self.ySlot = <int>(y // 16)
        self.zSlot = <int>(z // 16)
        if self.xSlot < 0:
            self.xSlot = 0
        if self.ySlot < 0:
            self.ySlot = 0
        if self.zSlot < 0:
            self.zSlot = 0

        if self.xSlot >= self.__entityMap.width:
            self.xSlot = self.__entityMap.width - 1
        if self.ySlot >= self.__entityMap.depth:
            self.ySlot = self.__entityMap.depth - 1
        if self.zSlot >= self.__entityMap.height:
            self.zSlot = self.__entityMap.height - 1

        return self

    cdef add(self, entity):
        if self.xSlot >= 0 and self.ySlot >= 0 and self.zSlot >= 0:
            self.__entityMap.entityGrid[(self.zSlot * self.__entityMap.depth + self.ySlot) * \
                                        self.__entityMap.width + self.xSlot].append(entity)

    cdef remove(self, entity):
        if self.xSlot >= 0 and self.ySlot >= 0 and self.zSlot >= 0:
            try:
                self.__entityMap.entityGrid[(self.zSlot * self.__entityMap.depth + self.ySlot) * \
                                            self.__entityMap.width + self.xSlot].remove(entity)
            except:
                pass
