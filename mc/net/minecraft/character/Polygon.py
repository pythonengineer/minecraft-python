from pyglet import gl

class Polygon:

    def __init__(self, vertices, u0=0, v0=0, u1=0, v1=0):
        self.vertices = vertices
        self.vertexCount = len(vertices)

        if u0 or v0 or u1 or v1:
            vertices[0] = vertices[0].remap(u1, v0)
            vertices[1] = vertices[1].remap(u0, v0)
            vertices[2] = vertices[2].remap(u0, v1)
            vertices[3] = vertices[3].remap(u1, v1)

    def render(self):
        gl.glColor3f(1.0, 1.0, 1.0)
        for i in range(3, -1, -1):
            v = self.vertices[i]
            gl.glTexCoord2f(v.u / 64.0, v.v / 32.0)
            gl.glVertex3f(v.pos.x, v.pos.y, v.pos.z)
