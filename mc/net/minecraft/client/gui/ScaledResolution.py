class ScaledResolution:

    def __init__(self, width, height):
        self.__scaledWidth = width
        self.__scaledHeight = height
        scale = 1
        while self.__scaledWidth // (scale + 1) >= 320 and \
              self.__scaledHeight // (scale + 1) >= 240:
            scale += 1

        self.__scaledWidth //= scale
        self.__scaledHeight //= scale

    def getScaledWidth(self):
        return self.__scaledWidth

    def getScaledHeight(self):
        return self.__scaledHeight
