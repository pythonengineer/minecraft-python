from mc.net.minecraft.client.model.md3.MD3FrameArray import MD3FrameArray
from mc.net.minecraft.client.model.md3.MD3Vertices import MD3Vertices
from mc.net.minecraft.client.model.md3.MD3Buffers import MD3Buffers
from mc.net.minecraft.client.model.md3.MD3Shader import MD3Shader
from mc.net.minecraft.client.model.md3.MD3Data import MD3Data
from mc.net.minecraft.game.physics.Vec3D import Vec3D
from mc.InputStream import ByteArrayOutputStream, DataInputStream
from mc.CompatibilityShims import BufferUtils, ByteOrder
from pyglet import resource

import math

class MD3Loader:

    def loadModel(self, fileName):
        data = DataInputStream(resource.file(f'md3/{fileName}', 'rb'))
        output = ByteArrayOutputStream()
        array = bytearray(4096)

        while True:
            length = data.read(array)
            if length < 0:
                data.close()
                output.close()
                buffer = BufferUtils.wrapByteBuffer(output.toByteArray())
                return self.__loadMD3Data(buffer)

            output.write(array, 0, length)

    def __loadMD3Data(self, buffer):
        buffer.order(ByteOrder.LITTLE_ENDIAN)
        header = MD3Loader.__loadMD3Info(buffer, 4)
        vertices = None
        if header != 'IDP3':
            raise IOError('Not a valid MD3 file (bad magic number)')
        else:
            vertices = MD3Vertices()
            buffer.getInt()
            MD3Loader.__loadMD3Info(buffer, 64)
            buffer.getInt()
            frames = buffer.getInt()
            print(frames, 'frames')
            tags = buffer.getInt()
            buffers = buffer.getInt()
            buffer.getInt()
            ofsFrames = buffer.getInt()
            buffer.getInt()
            ofsSurfaces = buffer.getInt()
            buffer.getInt()
            vertices.totalFrames = frames
            vertices.frameArray = [None] * frames
            vertices.modelMap = {}
            vertices.buffersMD3 = [None] * buffers
            buffer.position(ofsFrames)

            for frame in range(frames):
                frameArray = vertices.frameArray
                md3FrameArray = MD3FrameArray()
                MD3Loader.__getMD3Vec(buffer)
                MD3Loader.__getMD3Vec(buffer)
                MD3Loader.__getMD3Vec(buffer)
                buffer.getFloat()
                MD3Loader.__loadMD3Info(buffer, 16)
                frameArray[frame] = md3FrameArray

            md3Data = [None] * tags

            for i in range(tags):
                md3Data[i] = MD3Data(frames)

            for i in range(frames):
                for tag in range(tags):
                    data = md3Data[tag]
                    data.name = MD3Loader.__loadMD3Info(buffer, 64)
                    data.b[i] = MD3Loader.__getMD3Vec(buffer)
                    data.c[i] = MD3Loader.__getMD3Vec(buffer)
                    data.d[i] = MD3Loader.__getMD3Vec(buffer)
                    data.e[i] = MD3Loader.__getMD3Vec(buffer)

            for i in range(tags):
                vertices.modelMap[md3Data[i].name] = md3Data[i]

            buffer.position(ofsSurfaces)

            for i in range(buffers):
                vertices.buffersMD3[i] = self.__getMD3Buffer(buffer)

            return vertices

    def __getMD3Buffer(self, buffer):
        ofsSurfaces = buffer.position()
        header = MD3Loader.__loadMD3Info(buffer, 4)
        if header != 'IDP3':
            raise IOError('Not a valid MD3 file (bad surface magic number)')
        else:
            name = MD3Loader.__loadMD3Info(buffer, 64)
            print('Name:', name)
            buffer.getInt()
            frames = buffer.getInt()
            shaders = buffer.getInt()
            verts = buffer.getInt()
            triangles = buffer.getInt()
            buffers = MD3Buffers(triangles, verts, frames)
            ofsTriangles = buffer.getInt() + ofsSurfaces
            ofsShaders = buffer.getInt() + ofsSurfaces
            ofsSt = buffer.getInt() + ofsSurfaces
            ofsSurfaces += buffer.getInt()
            buffer.getInt()
            buffers.verts = verts
            buffers.shaders = [None] * shaders
            print('Triangles:', triangles)
            print('OFS_SHADERS:', ofsShaders, '(current location:', str(buffer.position()) + ')')
            buffer.position(ofsShaders)

            for i in range(shaders):
                shader = MD3Shader()
                MD3Loader.__loadMD3Info(buffer, 64)
                buffer.getInt()
                buffers.shaders[i] = shader

            print('OFS_TRIANGLES:', ofsTriangles, '(current location:', str(buffer.position()) + ')')
            buffer.position(ofsTriangles)

            for i in range(triangles * 3):
                buffers.triangles.put(buffer.getInt())

            print('OFS_ST:', ofsSt, '(current location:', str(buffer.position()) + ')')
            buffer.position(ofsSt)

            for i in range(verts << 1):
                buffers.xBuffer.put(buffer.getFloat())

            print('OFS_XYZ_NORMAL:', ofsSurfaces, '(current location:', str(buffer.position()) + ')')
            buffer.position(ofsSurfaces)

            for i in range(verts * frames):
                buffers.vertices.put(buffer.getShort() / 64.0)
                buffers.vertices.put(buffer.getShort() / 64.0)
                buffers.vertices.put(buffer.getShort() / 64.0)
                lat = (buffer.get() & 255) * math.pi * 2.0 / 255.0
                lng = (buffer.get() & 255) * math.pi * 2.0 / 255.0
                x = math.cos(lng) * math.sin(lat)
                y = math.sin(lng) * math.sin(lat)
                z = math.cos(lat)
                buffers.normals.put(x)
                buffers.normals.put(y)
                buffers.normals.put(z)

            return buffers

    @staticmethod
    def __getMD3Vec(buffer):
        return Vec3D(buffer.getFloat(), buffer.getFloat(), buffer.getFloat())

    @staticmethod
    def __loadMD3Info(buffer, size):
        b = bytearray(size)
        buffer.getBytes(b)

        for i in range(len(b)):
            if b[i] == 0:
                return b[:i].decode('utf-8')

        return b.decode('utf-8')
