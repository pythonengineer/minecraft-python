from pyglet import gl

class Polygon:

    def __init__(self, vertices, u0=0, v0=0, u1=0, v1=0):
        self.vertices = vertices
        if u0 or v0 or u1 or v1:
            vertices[0] = vertices[0].remap(u1, v0)
            vertices[1] = vertices[1].remap(u0, v0)
            vertices[2] = vertices[2].remap(u0, v1)
            vertices[3] = vertices[3].remap(u1, v1)
