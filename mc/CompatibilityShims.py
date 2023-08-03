from pyglet import gl

import ctypes
import struct
import math
import time

def getMillis():
    return int(round(time.time() * 1000))

def getNs():
    return time.time_ns()

def rshift(val, n):
    return (val % 0x100000000) >> n

def gluPerspective(fovY, aspect, zNear, zFar):
    fH = math.tan(fovY / 360 * math.pi) * zNear
    fW = fH * aspect

    gl.glFrustum(-fW, fW, -fH, fH, zNear, zFar)

class DataInputStream:

    def __init__(self, stream):
        self.stream = stream

    def close(self):
        self.stream.close()

    def readFully(self, array=None):
        data = self.stream.read()
        if not array:
            return data

        for i, element in enumerate(data):
            array[i] = element

    def readBoolean(self):
        return struct.unpack('?', self.stream.read(1))[0]

    def readByte(self):
        return struct.unpack('b', self.stream.read(1))[0]

    def readUnsignedByte(self):
        return struct.unpack('B', self.stream.read(1))[0]

    def readChar(self):
        return chr(struct.unpack('>H', self.stream.read(2))[0])

    def readDouble(self):
        return struct.unpack('>d', self.stream.read(8))[0]

    def readFloat(self):
        return struct.unpack('>f', self.stream.read(4))[0]

    def readShort(self):
        return struct.unpack('>h', self.stream.read(2))[0]

    def readUnsignedShort(self):
        return struct.unpack('>H', self.stream.read(2))[0]

    def readLong(self):
        return struct.unpack('>q', self.stream.read(8))[0]

    def readUTF(self):
        utfLength = struct.unpack('>H', self.stream.read(2))[0]
        return self.stream.read(utfLength).decode('utf-8')

    def readInt(self):
        return struct.unpack('>i', self.stream.read(4))[0]

class DataOutputStream:

    def __init__(self, stream):
        self.stream = stream

    def close(self):
        self.stream.close()

    def write(self, data):
        self.stream.write(data)

    def writeBoolean(self, boolean):
        self.stream.write(struct.pack('?', boolean))

    def writeByte(self, val):
        self.stream.write(struct.pack('b', val))

    def writeUnsignedByte(self, val):
        self.stream.write(struct.pack('B', val))

    def writeChar(self, val):
        self.stream.write(struct.pack('>H', ord(val)))

    def writeDouble(self, val):
        self.stream.write(struct.pack('>d', val))

    def writeFloat(self, val):
        self.stream.write(struct.pack('>f', val))

    def writeShort(self, val):
        self.stream.write(struct.pack('>h', val))

    def writeUnsignedShort(self, val):
        self.stream.write(struct.pack('>H', val))

    def writeLong(self, val):
        self.stream.write(struct.pack('>q', val))

    def writeUTF(self, string):
        self.stream.write(struct.pack('>H', len(string)))
        self.stream.write(string)

    def writeInt(self, val):
        self.stream.write(struct.pack('>i', val))

    def writeUnsignedInt(self, val):
        self.stream.write(struct.pack('>I', val))

class ByteArrayInputStream:

    def __init__(self, byteArray):
        self.byteArray = byteArray

    def read(self, size=None):
        if size:
            data = self.byteArray[:size]
            self.byteArray = self.byteArray[size:]
            return data
        else:
            return self.byteArray

    def close(self):
        pass

class ByteArrayOutputStream:

    def __init__(self):
        self.byteArray = bytearray()

    def toByteArray(self):
        return self.byteArray

    def write(self, data, off, length):
        for i in range(length):
            self.byteArray.append(data[i])

    def close(self):
        pass

class BufferUtils:

    def _get(array, x):
        if x is not None:
            if hasattr(x, '__iter__'):
                assert array.checkBounds(0, len(x), len(x))
                assert array._position <= array._limit
                rem = array._limit - array._position if array._position <= array._limit else 0
                if len(x) > rem:
                    raise Exception

                if isinstance(x, bytearray):
                    sliced = array[array._position:array._position + len(x)]
                    x[:] = [ctypes.c_ubyte(e).value for e in sliced]
                else:
                    x[:] = array[array._position:array._position + len(x)]

                array._position += len(x)
                return array
            elif isinstance(x, int):
                x = array.checkIndex(x)
                return array[x]
            else:
                raise Exception

        return array[array.nextGetIndex()]

    def _getLong(array):
        pos = array.nextGetIndex(1 << 3)

        return ((array[pos + 7] & 0xFF)      ) + \
               ((array[pos + 6] & 0xFF) <<  8) + \
               ((array[pos + 5] & 0xFF) << 16) + \
               ((array[pos + 4] & 0xFF) << 24) + \
               ((array[pos + 3] & 0xFF) << 32) + \
               ((array[pos + 2] & 0xFF) << 40) + \
               ((array[pos + 1] & 0xFF) << 48) + \
               (array[pos]              << 56)

    def _getInt(array):
        pos = array.nextGetIndex(1 << 2)

        return ((array[pos + 3] & 0xFF)      ) + \
               ((array[pos + 2] & 0xFF) << 8 ) + \
               ((array[pos + 1] & 0xFF) << 16) + \
               (array[pos]              << 24)

    def _getShort(array):
        pos = array.nextGetIndex(1 << 1)

        return ((array[pos + 1] & 0xFF)) + \
                (array[pos]        << 8)

    def _getDouble(array):
        pos = array.nextGetIndex(1 << 3)

        return struct.unpack('d', (
                   ((array[pos + 7] & 0xFF)      ) + \
                   ((array[pos + 6] & 0xFF) <<  8) + \
                   ((array[pos + 5] & 0xFF) << 16) + \
                   ((array[pos + 4] & 0xFF) << 24) + \
                   ((array[pos + 3] & 0xFF) << 32) + \
                   ((array[pos + 2] & 0xFF) << 40) + \
                   ((array[pos + 1] & 0xFF) << 48) + \
                   (array[pos]              << 56)))[0]

    def _put(array, x, y, z):
        if y is None:
            if hasattr(x, '__iter__'):
                array.put(x, 0, len(x))
            else:
                array[array.nextPutIndex()] = x
        elif z != None:
            assert array.checkBounds(y, z, len(x))
            assert array._position <= array._limit
            rem = array._limit - array._position if array._position <= array._limit else 0
            if z > rem:
                raise Exception

            for i, n in enumerate(range(y, y + z)):
                array[array._position + n] = x[i]

            array._position += z
        else:
            x = array.checkIndex(x)
            array[x] = y

        return array

    def _putLong(array, x):
        pos = array.nextPutIndex(1 << 3)

        array[pos + 7] = ctypes.c_ubyte(x).value
        array[pos + 6] = ctypes.c_ubyte(rshift(x, 8)).value
        array[pos + 5] = ctypes.c_ubyte(rshift(x, 16)).value
        array[pos + 4] = ctypes.c_ubyte(rshift(x, 24)).value
        array[pos + 3] = ctypes.c_ubyte(rshift(x, 32)).value
        array[pos + 2] = ctypes.c_ubyte(rshift(x, 40)).value
        array[pos + 1] = ctypes.c_ubyte(rshift(x, 48)).value
        array[pos    ] = ctypes.c_ubyte(rshift(x, 56)).value

        return array

    def _putInt(array, x):
        pos = array.nextPutIndex(1 << 2)

        array[pos + 3] = ctypes.c_ubyte(x).value
        array[pos + 2] = ctypes.c_ubyte(rshift(x, 8)).value
        array[pos + 1] = ctypes.c_ubyte(rshift(x, 16)).value
        array[pos    ] = ctypes.c_ubyte(rshift(x, 24)).value

        return array

    def _putShort(array, x):
        pos = array.nextPutIndex(1 << 1)

        array[pos + 1] = ctypes.c_ubyte(x).value
        array[pos    ] = ctypes.c_ubyte(rshift(x, 8)).value

        return array

    def _putDouble(array, x):
        pos = array.nextPutIndex(1 << 3)

        x = struct.pack('d', x)[0]

        array[pos + 7] = ctypes.c_ubyte(x).value
        array[pos + 6] = ctypes.c_ubyte(rshift(x, 8)).value
        array[pos + 5] = ctypes.c_ubyte(rshift(x, 16)).value
        array[pos + 4] = ctypes.c_ubyte(rshift(x, 24)).value
        array[pos + 3] = ctypes.c_ubyte(rshift(x, 32)).value
        array[pos + 2] = ctypes.c_ubyte(rshift(x, 40)).value
        array[pos + 1] = ctypes.c_ubyte(rshift(x, 48)).value
        array[pos    ] = ctypes.c_ubyte(rshift(x, 56)).value

        return array

    def _flip(array):
        array._limit = array._position
        array._position = 0
        return array

    def _limit(array, limit):
        if limit < 0 or limit > len(array):
            return array

        array._limit = limit
        if array._position > limit:
            array._position = limit

        return array

    def _compact(array):
        assert array._position <= array._limit

        rem = array._limit - array._position if array._position <= array._limit else 0
        array[:rem] = array[array._position:array._position + rem]

        array._position = rem
        array._limit = len(array)

        return array

    def _position(array, position):
        if position is None:
            return array._position
        if position < 0 or position >= len(array):
            raise Exception
        if position > array._limit:
            raise Exception

        array._position = position
        return array

    def _clear(array):
        array._position = 0
        array._limit = len(array)
        return array

    def _nextIndex(array, nb=None):
        if nb is not None:
            if array._limit - array._position < nb:
                raise Exception
        elif array._position >= array._limit:
            raise Exception

        if nb is None:
            nb = 1

        p = array._position
        array._position += nb
        return p

    def _checkIndex(array, i):
        if i < 0 or i >= array._limit:
            raise Exception

        return i

    def _checkBounds(off, length, size):
        if (off | length | (off + length) | (size - (off + length))) < 0:
            raise Exception

        return True

    def extend(obj):
        obj.get = lambda x=None: BufferUtils._get(obj, x)
        obj.getLong = lambda: BufferUtils._getLong(obj)
        obj.getInt = lambda: BufferUtils._getInt(obj)
        obj.getShort = lambda: BufferUtils._getShort(obj)
        obj.getDouble = lambda: BufferUtils._getDouble(obj)
        obj.getFloat = lambda: BufferUtils._getDouble(obj)
        obj.put = lambda x, y=None, z=None: BufferUtils._put(obj, x, y, z)
        obj.putLong = lambda x: BufferUtils._putLong(obj, x)
        obj.putInt = lambda x: BufferUtils._putInt(obj, x)
        obj.putShort = lambda x: BufferUtils._putShort(obj, x)
        obj.putDouble = lambda x: BufferUtils._putDouble(obj, x)
        obj.putFloat = lambda x: BufferUtils._putDouble(obj, x)
        obj.flip = lambda: BufferUtils._flip(obj)
        obj.limit = lambda limit: BufferUtils._limit(obj, limit)
        obj.compact = lambda: BufferUtils._compact(obj)
        obj.position = lambda position=None: BufferUtils._position(obj, position)
        obj.remaining = lambda: obj._limit - obj._position
        obj.clear = lambda: BufferUtils._clear(obj)
        obj.capacity = lambda: len(obj)
        obj.nextGetIndex = lambda x=None: BufferUtils._nextIndex(obj, x)
        obj.nextPutIndex = lambda x=None: BufferUtils._nextIndex(obj, x)
        obj.checkIndex = lambda x: BufferUtils._checkIndex(obj, x)
        obj.checkBounds = lambda x, y, z: BufferUtils._checkBounds(x, y, z)
        return obj

    def createByteBuffer(capacity):
        return BufferUtils.extend((ctypes.c_byte * capacity)())

    def createUintBuffer(capacity):
        return BufferUtils.extend((gl.GLuint * capacity)())

    def createIntBuffer(capacity):
        return BufferUtils.extend((gl.GLint * capacity)())

    def createFloatBuffer(capacity):
        return BufferUtils.extend((gl.GLfloat * capacity)())
