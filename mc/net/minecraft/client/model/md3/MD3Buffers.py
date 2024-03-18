from mc.CompatibilityShims import BufferUtils

class MD3Buffers:

    def __init__(self, triangles, verts, frames):
        self.verts = verts
        self.frames = frames
        self.triangles = BufferUtils.createIntBuffer(triangles * 3)
        self.xBuffer = BufferUtils.createFloatBuffer(verts << 1)
        self.vertices = BufferUtils.createFloatBuffer(verts * (frames + 2) * 3)
        self.normals = BufferUtils.createFloatBuffer(verts * (frames + 2) * 3)
        self.__data1 = [0.0] * verts * 3
        self.__data2 = [0.0] * verts * 3
        self.shaders = []
