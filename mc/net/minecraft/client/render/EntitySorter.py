class EntitySorter:

    def __init__(self, player):
        self.__player = player

    def compare(self, chunk1, chunk2):
        return -1 if chunk1.distanceToEntitySquared(self.__player) < chunk2.distanceToEntitySquared(self.__player) else 1
