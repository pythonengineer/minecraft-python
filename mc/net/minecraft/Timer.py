from mc.CompatibilityShims import getMillis, getNs

class Timer:
    NS_PER_SECOND = 1000000
    MAX_TICKS_PER_UPDATE = 100
    lastTime = 0.0
    frames = 0
    alpha = 0.0
    fps = 1.0
    ticks = 0.0
    averageFrameTime = 1.0

    def __init__(self, ticksPerSecond):
        self.ticksPerSecond = ticksPerSecond
        self.msPerTick = getMillis()
        self.passedTime = getNs() // self.NS_PER_SECOND
