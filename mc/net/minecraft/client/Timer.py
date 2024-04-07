from mc.CompatibilityShims import getMillis

import time

class Timer:
    NS_PER_SECOND = 1000000
    MAX_TICKS_PER_UPDATE = 100
    __lastHRTime = 0.0
    elapsedTicks = 0
    renderPartialTicks = 0.0
    __delta = 1.0
    __elapsedPartialTicks = 0.0
    __timeSyncAdjustment = 1.0

    def __init__(self, ticksPerSecond):
        self.ticksPerSecond = 20.0
        self.__lastSyncSysClock = getMillis()
        self.__lastSyncHRClock = time.time_ns() // Timer.NS_PER_SECOND

    def updateTimer(self):
        now = getMillis()
        passedMs = now - self.__lastSyncSysClock
        timeRate = time.time_ns() // Timer.NS_PER_SECOND
        if passedMs > 1000:
            syncDelta = timeRate - self.__lastSyncHRClock
            adjust = passedMs / syncDelta
            self.__timeSyncAdjustment += (adjust - self.__timeSyncAdjustment) * 0.2
            self.__lastSyncSysClock = now
            self.__lastSyncHRClock = timeRate
        elif passedMs < 0:
            self.__lastSyncSysClock = now
            self.__lastSyncHRClock = timeRate

        hrTime = timeRate / 1000.0
        adjust = (hrTime - self.__lastHRTime) * self.__timeSyncAdjustment
        self.__lastHRTime = hrTime
        if adjust < 0.0:
            adjust = 0.0
        elif adjust > 1.0:
            adjust = 1.0

        self.__elapsedPartialTicks += adjust * self.__delta * self.ticksPerSecond
        self.elapsedTicks = int(self.__elapsedPartialTicks)
        if self.elapsedTicks > Timer.MAX_TICKS_PER_UPDATE:
            self.elapsedTicks = Timer.MAX_TICKS_PER_UPDATE

        self.__elapsedPartialTicks -= self.elapsedTicks
        self.renderPartialTicks = self.__elapsedPartialTicks
