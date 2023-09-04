from mc.net.minecraft.player.Input import Input
from pyglet import window

class KeyboardInput(Input):

    def __init__(self, options):
        self.__options = options
        self.__keys = [False] * 10

    def setKey(self, symbol, state):
        id_ = -1
        if symbol == self.__options.forward.key: id_ = 0
        if symbol == self.__options.back.key: id_ = 1
        if symbol == self.__options.left.key: id_ = 2
        if symbol == self.__options.right.key: id_ = 3
        if symbol == self.__options.jump.key: id_ = 4
        if id_ >= 0:
            self.__keys[id_] = state

    def releaseAllKeys(self):
        for i in range(10):
            self.__keys[i] = False

    def tick(self):
        self.ya = 0.0
        self.xa = 0.0
        if self.__keys[0]: self.xa -= 1.0
        if self.__keys[1]: self.xa += 1.0
        if self.__keys[2]: self.ya -= 1.0
        if self.__keys[3]: self.ya += 1.0

        self.jumping = self.__keys[4]
