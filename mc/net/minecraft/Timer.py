from mc.CompatibilityShims import getNs

class Timer:
    NS_PER_SECOND = 1000000000
    MAX_NS_PER_UPDATE = 1000000000
    MAX_TICKS_PER_UPDATE = 100
    ticks = 0
    a = 0.0
    timeScale = 1.0
    fps = 0.0
    passedTime = 0.0

    def __init__(self, ticksPerSecond):
        self.__ticksPerSecond = ticksPerSecond
        self.__lastTime = getNs()

    def advanceTime(self):
        now = getNs()
        passedNs = now - self.__lastTime
        self.__lastTime = now

        if passedNs < 0:
            passedNs = 1
        elif passedNs > self.MAX_NS_PER_UPDATE:
            passedNs = self.MAX_NS_PER_UPDATE
        elif passedNs == 0:
            passedNs = 1
        self.fps = self.NS_PER_SECOND / passedNs

        self.passedTime += passedNs * self.timeScale * self.__ticksPerSecond / float(self.NS_PER_SECOND)

        self.ticks = int(self.passedTime)
        if self.ticks > self.MAX_TICKS_PER_UPDATE:
            self.ticks = self.MAX_TICKS_PER_UPDATE
        self.passedTime -= self.ticks
        self.a = self.passedTime
