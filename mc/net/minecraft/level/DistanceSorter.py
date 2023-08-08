class DistanceSorter:

    def __init__(self, player):
        self.__player = player

    def compare(self, c0, c1):
        return -1 if c0.distanceToSqr(self.__player) < c1.distanceToSqr(self.__player) else 1
