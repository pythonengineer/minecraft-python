from mc.CompatibilityShims import DataInputStream, DataOutputStream

class LevelIO:
    MAGIC_NUMBER = 656127880
    CURRENT_VERSION = 1

    def __init__(self, minecraft):
        self.__minecraft = minecraft

    def load(self, level, inp):
        self.__minecraft.beginLevelLoading('Loading level')
        self.__minecraft.levelLoadUpdate('Reading..')
        try:
            dis = DataInputStream(inp)
            magic = dis.readInt()
            if magic != self.MAGIC_NUMBER:
                return False
            version = dis.readByte()
            if version > self.CURRENT_VERSION:
                return False

            name = dis.readUTF()
            creator = dis.readUTF()
            createTime = dis.readLong()

            width = dis.readShort()
            height = dis.readShort()
            depth = dis.readShort()

            blocks = bytearray(dis.readFully())
            dis.close()

            level.setDataBytes(width, depth, height, blocks)
            level.name = name
            level.creator = creator
            level.createTime = createTime
            return True
        except Exception as e:
            print('Failed to load level:', e)

        return False

    def loadLegacy(self, level, inp):
        self.__minecraft.beginLevelLoading('Loading level')
        self.__minecraft.levelLoadUpdate('Reading..')
        try:
            dis = DataInputStream(inp)

            name = '--'
            creator = 'unknown'
            createTime = 0

            width = 256
            height = 256
            depth = 64

            blocks = bytearray(dis.readFully())
            dis.close()

            level.setDataBytes(width, depth, height, blocks)
            level.name = name
            level.creator = creator
            level.createTime = createTime
            return True
        except Exception as e:
            print('Failed to load level:', e)

        return False

    @staticmethod
    def save(level, out):
        dos = DataOutputStream(out)
        dos.writeInt(LevelIO.MAGIC_NUMBER)
        dos.writeByte(LevelIO.CURRENT_VERSION)
        dos.writeUTF(level.name.encode())
        dos.writeUTF(level.creator.encode())
        dos.writeLong(level.createTime)
        dos.writeShort(level.width)
        dos.writeShort(level.height)
        dos.writeShort(level.depth)
        dos.write(level.getBlocks())
        dos.close()
