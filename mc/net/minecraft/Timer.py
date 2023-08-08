from mc.CompatibilityShims import getNs

class Timer:
    NS_PER_SECOND = 1000000000
    MAX_NS_PER_UPDATE = 1000000000
    MAX_TICKS_PER_UPDATE = 100
    ticks = 0
    a = 0.0
    timeScale = 1.0
    fps = 0.0

    def __init__(self, ticksPerSecond):
        self.ticksPerSecond = ticksPerSecond
        self.lastTime = getNs()
