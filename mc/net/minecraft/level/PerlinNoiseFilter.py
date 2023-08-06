import random
import math

class PerlinNoiseFilter:
    seed = random.random()
    fuzz = 16

    def __init__(self, levels):
        self.levels = levels

    def read(self, width, height):
        tmp = [0] * (width * height)
        level = self.levels
        step = width >> level
        for y in range(0, height, step):
            for x in range(0, width, step):
                tmp[x + y * width] = (math.floor(256 * random.random()) - 128) * self.fuzz

        while step > 1:
            val = 256 * (step << level)
            ss = step // 2

            for y in range(0, height, step):
                for x in range(0, width, step):
                    ul = tmp[(x + 0) % width + (y + 0) % height * width]
                    ur = tmp[(x + step) % width + (y + 0) % height * width]
                    dl = tmp[(x + 0) % width + (y + step) % height * width]
                    dr = tmp[(x + step) % width + (y + step) % height * width]

                    m = (ul + dl + ur + dr) // 4 + math.floor((val * 2) * random.random()) - val

                    tmp[x + ss + (y + ss) * width] = m

            for y in range(0, height, step):
                for x in range(0, width, step):
                    c = tmp[x + y * width]
                    r = tmp[(x + step) % width + y * width]
                    d = tmp[x + (y + step) % width * width]

                    mu = tmp[(x + ss & width - 1) + (y + ss - step & height - 1) * width]
                    ml = tmp[(x + ss - step & width - 1) + (y + ss & height - 1) * width]
                    m = tmp[(x + ss) % width + (y + ss) % height * width]

                    u = (c + r + m + mu) // 4 + math.floor((val * 2) * random.random()) - val
                    l = (c + d + m + ml) // 4 + math.floor((val * 2) * random.random()) - val

                    tmp[x + ss + y * width] = u
                    tmp[x + (y + ss) * width] = l

            step //= 2

        result = [0] * (width * height)
        for y in range(height):
            for x in range(width):
                result[x + y * width] = tmp[x % width + y % height * width] // 512 + 128

        return result
