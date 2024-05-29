class ScaledResolution:

    def __init__(self, width, height):
        self.__scaledWidth = width
        self.__scaledHeight = height
        while self.__scaledWidth >= 640 and self.__scaledHeight >= 480:
            self.__scaledWidth //= 2
            self.__scaledHeight //= 2

    def getScaledWidth(self):
        return self.__scaledWidth

    def getScaledHeight(self):
        return self.__scaledHeight
