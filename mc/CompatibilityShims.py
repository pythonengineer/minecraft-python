import abc
import ctypes
import math
import struct
import textwrap
import time

from pyglet import gl as opengl


def getMillis():
    return int(round(time.time() * 1000))


def getNs():
    return time.time_ns()


def rshift(value, n):
    return (value % pow(2, 32)) >> n


def gluPerspective(fovY, aspect, zNear, zFar):
    fH = math.tan(fovY / 360 * math.pi) * zNear
    fW = fH * aspect

    opengl.glFrustum(-fW, fW, -fH, fH, zNear, zFar)


class _Stream(abc.ABC):

    @abc.abstractmethod
    def read(self, n: int = -1):
        raise NotImplementedError()

    @abc.abstractmethod
    def write(self, data: bytes):
        raise NotImplementedError()

    @abc.abstractmethod
    def close(self):
        raise NotImplementedError()


class DataStream(_Stream):

    def __init__(self, stream):
        self.stream = stream

    def read(self, n: int = -1):
        return self.stream.read(n)

    def write(self, data: bytes):
        self.stream.write(data)

    def close(self):
        self.stream.close()

    for name, (format, size) in {'Boolean': ('?', 1),
                                 'Byte': ('b', 1),
                                 'UnsignedByte': ('B', 1),
                                 'Short': ('>h', 2),
                                 'UnsignedShort': ('>H', 2),
                                 'Int': ('>i', 4),
                                 'Float': ('>f', 4),
                                 'Long': ('>q', 8),
                                 'Double': ('>d', 8),
                                 }.items():
        exec(textwrap.dedent(f"""
        def read{name}():
            return struct.unpack({format!r}, self.read({size!r}))

        def write{name}(value):
            return self.write(struct.pack({format!r}, value))
        """))


class ByteArrayStream(_Stream):

    def __init__(self, buffer: bytearray = bytearray()):
        self._buffer = buffer

    def read(self, n: int = -1) -> bytearray:
        if n > 0:
            data = self._buffer[:n]
            self._buffer = self._buffer[n:]
            return data
        else:
            return self._buffer

    def write(self, data: bytes):
        for elem in data:
            self._buffer.append(elem)

    def close(self):
        self._buffer = bytearray()


class BufferUtils:

    def _get(array, x):
        if x is None:
            return array[array.nextGetIndex()]

        if isinstance(x, int):
            x = array.checkIndex(x)
            return array[x]

        if not hasattr(x, '__iter__'):
            raise Exception()

        assert array.checkBounds(0, len(x), len(x))
        assert array._position <= array._limit

        if len(x) > ((array._limit - array._position)
                     if (array._position <= array._limit)
                     else 0
                     ):
            raise Exception()

        if isinstance(x, bytearray):
            sliced = array[array._position : array._position + len(x)]
            x[:] = [ctypes.c_ubyte(elem).value for elem in sliced]
        else:
            x[:] = array[array._position : array._position + len(x)]

        array._position += len(x)
        return array

    def _getShort(array):
        pos = array.nextGetIndex(1 << 1)
        return (
            (  (array[pos + 1] & 0xFF) << 0x00)
            + ((array[pos + 0] & 0xFF) << 0x08)
            )

    def _getInt(array):
        pos = array.nextGetIndex(1 << 2)
        return (
            (  (array[pos + 3] & 0xFF) << 0x00)
            + ((array[pos + 2] & 0xFF) << 0x08)
            + ((array[pos + 1] & 0xFF) << 0x10)
            + ((array[pos + 0] & 0xFF) << 0x18)
            )

    def _getLong(array):
        pos = array.nextGetIndex(1 << 3)
        return (
            (  (array[pos + 7] & 0xFF) << 0x00)
            + ((array[pos + 6] & 0xFF) << 0x08)
            + ((array[pos + 5] & 0xFF) << 0x10)
            + ((array[pos + 4] & 0xFF) << 0x18)
            + ((array[pos + 3] & 0xFF) << 0x20)
            + ((array[pos + 2] & 0xFF) << 0x28)
            + ((array[pos + 1] & 0xFF) << 0x30)
            + ((array[pos + 0] & 0xFF) << 0x38)
            )

    def _getDouble(array):
        pos = array.nextGetIndex(1 << 3)
        return struct.unpack('d', (
            (  (array[pos + 7] & 0xFF) << 0x00)
            + ((array[pos + 6] & 0xFF) << 0x08)
            + ((array[pos + 5] & 0xFF) << 0x10)
            + ((array[pos + 4] & 0xFF) << 0x18)
            + ((array[pos + 3] & 0xFF) << 0x20)
            + ((array[pos + 2] & 0xFF) << 0x28)
            + ((array[pos + 1] & 0xFF) << 0x30)
            + ((array[pos + 0] & 0xFF) << 0x38)
            ))[0]

    def _put(array, x, y, z):
        if y is None:
            if not hasattr(x, '__iter__'):
                array[array.nextPutIndex()] = x
            else:
                array.put(x, 0, len(x))

        elif z is None:
            x = array.checkIndex(x)
            array[x] = y

        else:
            assert array.checkBounds(y, z, len(x))
            assert (array._position <= array._limit)

            if z > ((array._limit - array._position)
                    if (array._position <= array._limit)
                    else 0
                    ):
                raise Exception

            for i, n in enumerate(range(y, y + z)):
                array[array._position + n] = x[i]

            array._position += z

        return array

    def _putShort(array, x):
        pos = array.nextPutIndex(1 << 1)
        array[pos + 1] = ctypes.c_ubyte(rshift(x, 0x00)).value
        array[pos + 0] = ctypes.c_ubyte(rshift(x, 0x08)).value
        return array

    def _putInt(array, x):
        pos = array.nextPutIndex(1 << 2)
        array[pos + 3] = ctypes.c_ubyte(rshift(x, 0x00)).value
        array[pos + 2] = ctypes.c_ubyte(rshift(x, 0x08)).value
        array[pos + 1] = ctypes.c_ubyte(rshift(x, 0x10)).value
        array[pos + 0] = ctypes.c_ubyte(rshift(x, 0x18)).value
        return array

    def _putLong(array, x):
        pos = array.nextPutIndex(1 << 3)
        array[pos + 7] = ctypes.c_ubyte(rshift(x, 0x00)).value
        array[pos + 6] = ctypes.c_ubyte(rshift(x, 0x08)).value
        array[pos + 5] = ctypes.c_ubyte(rshift(x, 0x10)).value
        array[pos + 4] = ctypes.c_ubyte(rshift(x, 0x18)).value
        array[pos + 3] = ctypes.c_ubyte(rshift(x, 0x20)).value
        array[pos + 2] = ctypes.c_ubyte(rshift(x, 0x28)).value
        array[pos + 1] = ctypes.c_ubyte(rshift(x, 0x30)).value
        array[pos + 0] = ctypes.c_ubyte(rshift(x, 0x38)).value
        return array

    def _putDouble(array, x):
        pos = array.nextPutIndex(1 << 3)
        x = struct.pack('d', x)[0]
        array[pos + 7] = ctypes.c_ubyte(rshift(x, 0x00)).value
        array[pos + 6] = ctypes.c_ubyte(rshift(x, 0x08)).value
        array[pos + 5] = ctypes.c_ubyte(rshift(x, 0x10)).value
        array[pos + 4] = ctypes.c_ubyte(rshift(x, 0x18)).value
        array[pos + 3] = ctypes.c_ubyte(rshift(x, 0x20)).value
        array[pos + 2] = ctypes.c_ubyte(rshift(x, 0x28)).value
        array[pos + 1] = ctypes.c_ubyte(rshift(x, 0x30)).value
        array[pos + 0] = ctypes.c_ubyte(rshift(x, 0x38)).value
        return array

    def _flip(array):
        array._limit = array._position
        array._position = 0
        return array

    def _limit(array, limit):
        if not ((limit < 0) or (limit > len(array))):
            array._limit = limit
            if array._position > limit:
                array._position = limit

        return array

    def _compact(array):
        assert array._position <= array._limit
        rem = ((array._limit - array._position)
               if (array._position <= array._limit)
               else 0
               )

        array[:rem] = array[array._position : array._position + rem]
        array._position = rem
        array._limit = len(array)
        return array

    def _position(array, position):
        if position is None:
            return array._position

        if ((position < 0)
              or (position >= len(array))
              or (position > array._limit)
              ):
            raise Exception()
        else:
            array._position = position
            return array

    def _clear(array):
        array._position = 0
        array._limit = len(array)
        return array

    def _nextIndex(array, nb = None):
        if nb is not None:
            if (array._limit - array._position) < nb:
                raise Exception()
        else:
            if (array._position >= array._limit):
                raise Exception()

        if nb is None:
            nb = 1

        p = array._position
        array._position += nb
        return p

    def _checkIndex(array, i):
        if (i < 0) or (i >= array._limit):
            raise Exception()
        else:
            return i

    def _checkBounds(off, length, size):
        if (off
            | length
            | (off + length)
            | (size - (off + length))
            ) < 0:
            raise Exception()
        else:
            return True

    def extend(obj):
        obj.get = lambda x = None: BufferUtils._get(obj, x)
        obj.getLong = lambda: BufferUtils._getLong(obj)
        obj.getInt = lambda: BufferUtils._getInt(obj)
        obj.getShort = lambda: BufferUtils._getShort(obj)
        obj.getDouble = lambda: BufferUtils._getDouble(obj)
        obj.getFloat = lambda: BufferUtils._getDouble(obj)

        obj.put = lambda x, y = None, z = None: BufferUtils._put(obj, x, y, z)
        obj.putLong = lambda x: BufferUtils._putLong(obj, x)
        obj.putInt = lambda x: BufferUtils._putInt(obj, x)
        obj.putShort = lambda x: BufferUtils._putShort(obj, x)
        obj.putDouble = lambda x: BufferUtils._putDouble(obj, x)
        obj.putFloat = lambda x: BufferUtils._putDouble(obj, x)

        obj.flip = lambda: BufferUtils._flip(obj)
        obj.limit = lambda limit: BufferUtils._limit(obj, limit)
        obj.compact = lambda: BufferUtils._compact(obj)
        obj.position = lambda position = None: BufferUtils._position(obj, position)
        obj.clear = lambda: BufferUtils._clear(obj)

        obj.remaining = lambda: (obj._limit - obj._position)
        obj.capacity = lambda: len(obj)

        obj.nextGetIndex = lambda x = None: BufferUtils._nextIndex(obj, x)
        obj.nextPutIndex = lambda x = None: BufferUtils._nextIndex(obj, x)
        obj.checkIndex = lambda x: BufferUtils._checkIndex(obj, x)
        obj.checkBounds = lambda x, y, z: BufferUtils._checkBounds(x, y, z)

        return obj

    def createByteBuffer(size):
        return BufferUtils.extend((ctypes.c_byte * size)())

    def createUintBuffer(size):
        return BufferUtils.extend((opengl.GLuint * size)())

    def createIntBuffer(size):
        return BufferUtils.extend((opengl.GLint * size)())

    def createFloatBuffer(size):
        return BufferUtils.extend((opengl.GLfloat * size)())
