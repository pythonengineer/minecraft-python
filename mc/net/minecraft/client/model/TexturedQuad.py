class TexturedQuad:

    def __init__(self, vertices, u0=None, v0=None, u1=None, v1=None):
        self.vertexPositions = vertices
        if isinstance(u0, int):
            vertices[0] = vertices[0].setTexturePosition(u1 / 64.0 - 0.0015625,
                                                         v0 / 32.0 + 0.003125)
            vertices[1] = vertices[1].setTexturePosition(u0 / 64.0 + 0.0015625,
                                                         v0 / 32.0 + 0.003125)
            vertices[2] = vertices[2].setTexturePosition(u0 / 64.0 + 0.0015625,
                                                         v1 / 32.0 - 0.003125)
            vertices[3] = vertices[3].setTexturePosition(u1 / 64.0 - 0.0015625,
                                                         v1 / 32.0 - 0.003125)
