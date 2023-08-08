class Synth:

    def getValue(self, paramDouble1, paramDouble2):
        pass

    def create(self, width, height):
        result = [0.0] * width * height
        for y in range(height):
            for x in range(width):
                result[x + y * width] = self.getValue(x, y)

        return result
