from pyglet import gl

class Polygon:

    def __init__(self, vertices, u0=None, v0=None, u1=None, v1=None):
        self.vertices = vertices
        if isinstance(u0, int):
            f = 0.0015625
            f2 = 0.003125
            vertices[0] = vertices[0].remap(u1 / 64.0 - f, v0 / 32.0 + f2)
            vertices[1] = vertices[1].remap(u0 / 64.0 + f, v0 / 32.0 + f2)
            vertices[2] = vertices[2].remap(u0 / 64.0 + f, v1 / 32.0 - f2)
            vertices[3] = vertices[3].remap(u1 / 64.0 - f, v1 / 32.0 - f2)
        elif isinstance(u0, float):
            vertices[0] = vertices[0].remap(u1, v0)
            vertices[1] = vertices[1].remap(u0, v0)
            vertices[2] = vertices[2].remap(u0, v1)
            vertices[3] = vertices[3].remap(u1, v1)
