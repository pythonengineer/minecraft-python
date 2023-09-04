# cython: language_level=3

cimport cython

@cython.final
cdef class Slot:

    def __init__(self, blockMap):
        self.xSlot = 0
        self.ySlot = 0
        self.zSlot = 0
        self.__blockInMapArray = blockMap

    cdef Slot init(self, float x, float y, float z):
        self.xSlot = <int>(x // 16)
        self.ySlot = <int>(y // 16)
        self.zSlot = <int>(z // 16)
        if self.xSlot < 0:
            self.xSlot = 0
        if self.ySlot < 0:
            self.ySlot = 0
        if self.zSlot < 0:
            self.zSlot = 0

        if self.xSlot >= self.__blockInMapArray.width:
            self.xSlot = self.__blockInMapArray.width - 1
        if self.ySlot >= self.__blockInMapArray.depth:
            self.ySlot = self.__blockInMapArray.depth - 1
        if self.zSlot >= self.__blockInMapArray.height:
            self.zSlot = self.__blockInMapArray.height - 1

        return self

    cdef add(self, entity):
        if self.xSlot >= 0 and self.ySlot >= 0 and self.zSlot >= 0:
            self.__blockInMapArray.entityGrid[(self.zSlot * self.__blockInMapArray.depth + self.ySlot) * \
                                              self.__blockInMapArray.width + self.xSlot].append(entity)

    cdef remove(self, entity):
        if self.xSlot >= 0 and self.ySlot >= 0 and self.zSlot >= 0:
            try:
                self.__blockInMapArray.entityGrid[(self.zSlot * self.__blockInMapArray.depth + self.ySlot) * \
                                                  self.__blockInMapArray.width + self.xSlot].remove(entity)
            except ValueError:
                pass
