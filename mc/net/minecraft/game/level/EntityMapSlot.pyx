# cython: language_level=3

cdef class EntityMapSlot:

    def __init__(self, entityMap):
        self.posX = 0
        self.posY = 0
        self.posZ = 0
        self.__entityMap = entityMap

    cdef EntityMapSlot init(self, float x, float y, float z):
        self.posX = <int>(x // 16)
        self.posY = <int>(y // 16)
        self.posZ = <int>(z // 16)
        if self.posX < 0:
            self.posX = 0
        if self.posY < 0:
            self.posY = 0
        if self.posZ < 0:
            self.posZ = 0

        if self.posX >= self.__entityMap.width:
            self.posX = self.__entityMap.width - 1
        if self.posY >= self.__entityMap.depth:
            self.posY = self.__entityMap.depth - 1
        if self.posZ >= self.__entityMap.height:
            self.posZ = self.__entityMap.height - 1

        return self

    cdef add(self, entity):
        if self.posX >= 0 and self.posY >= 0 and self.posZ >= 0:
            self.__entityMap.entityGrid[(self.posZ * self.__entityMap.depth + self.posY) * \
                                        self.__entityMap.width + self.posX].append(entity)

    cdef remove(self, entity):
        if self.posX >= 0 and self.posY >= 0 and self.posZ >= 0:
            try:
                self.__entityMap.entityGrid[(self.posZ * self.__entityMap.depth + self.posY) * \
                                            self.__entityMap.width + self.posX].remove(entity)
            except:
                pass
