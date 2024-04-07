from mc.CompatibilityShims import BufferUtils

class MD3Buffers:

    def __init__(self, triangles, verts, frames):
        self.verts = verts
        self.__frames = frames
        self.triangles = BufferUtils.createIntBuffer(triangles * 3)
        self.xBuffer = BufferUtils.createFloatBuffer(verts << 1)
        self.vertices = BufferUtils.createFloatBuffer(verts * (frames + 2) * 3)
        self.normals = BufferUtils.createFloatBuffer(verts * (frames + 2) * 3)
        self.__data1 = [0.0] * verts * 3
        self.__data2 = [0.0] * verts * 3
        self.shaders = []

    def setAndClearBuffers(self, x, y, z):
        self.triangles.position(0).limit(self.triangles.capacity())
        self.xBuffer.position(0).limit(self.xBuffer.capacity())
        frames = 0
        if z != 0.0:
            self.__setBuffer(self.vertices, x, y, z)
            self.__setBuffer(self.normals, x, y, z)
            frames = self.__frames

        self.vertices.clear().position(frames * self.verts * 3).limit((frames + 1) * self.verts * 3)
        self.normals.clear().position(frames * self.verts * 3).limit((frames + 1) * self.verts * 3)

    def __setBuffer(self, buffer, x, y, z):
        buffer.clear().position(x * self.verts * 3).limit((x + 1) * self.verts * 3)
        buffer.get(self.__data1)
        buffer.clear().position(y * self.verts * 3).limit((y + 1) * self.verts * 3)
        buffer.get(self.__data2)

        for i in range(self.verts * 3):
            self.__data1[i] += (self.__data2[i] - self.__data1[i]) * z

        x = self.__frames
        buffer.clear().position(x * self.verts * 3)
        buffer.putBytes(self.__data1)
