class RenderSorter:

    def __init__(self, player):
        self.__player = player

    def compare(self, chunk1, chunk2):
        if chunk1.isInFrustum and not chunk2.isInFrustum:
            return 1
        elif (not chunk2.isInFrustum or chunk1.isInFrustum) and \
             chunk1.distanceToEntitySquared(self.__player) < chunk2.distanceToEntitySquared(self.__player):
            return 1
        else:
            return -1
