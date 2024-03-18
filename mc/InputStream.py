import struct

class DataInputStream:

    def __init__(self, stream):
        self.stream = stream

    def close(self):
        self.stream.close()

    def read(self, array):
        data = self.stream.read(len(array))
        i = 0
        for i, element in enumerate(data):
            if i == len(array):
                break

            array[i] = element

        return -1 if i == 0 else i + 1

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
            self.byteArray.append(data[off + i])

    def close(self):
        pass
