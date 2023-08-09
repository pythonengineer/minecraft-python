class DirtyChunkSorter:

    def __init__(self, player):
        self.__player = player

    def compare(self, c0, c1):
        z3 = c0._isInFrustum
        z4 = c1._isInFrustum
        return -1 if z3 and not z4 else ((not z4 or z3) and -1 if c0.compare(self.__player) < c1.compare(self.__player) else 1)
