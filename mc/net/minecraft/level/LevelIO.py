from mc.net.minecraft.level.Level import Level
from mc.CompatibilityShims import DataInputStream, DataOutputStream
import pickle

class LevelIO:
    MAGIC_NUMBER = 656127880
    CURRENT_VERSION = 2

    def __init__(self, descriptorEvent):
        self.__levelLoaderListener = descriptorEvent

    def load(self, inp):
        self.__levelLoaderListener.beginLevelLoading('Loading level')
        self.__levelLoaderListener.levelLoadUpdate('Reading..')
        try:
            dis = DataInputStream(inp)
            magic = dis.readInt()
            if magic != LevelIO.MAGIC_NUMBER:
                dis.close()
                return None
            version = dis.readByte()
            if version > LevelIO.CURRENT_VERSION:
                dis.close()
                return None
            elif version == 1:
                name = dis.readUTF()
                creator = dis.readUTF()
                createTime = dis.readLong()

                width = dis.readShort()
                height = dis.readShort()
                depth = dis.readShort()

                blocks = bytearray(dis.readFully())
                dis.close()

                level = Level()
                level.setDataLegacy(width, depth, height, blocks)
                level.name = name
                level.creator = creator
                level.createTime = createTime
            else:
                level = pickle.loads(dis.readFully())

            dis.close()
            return level
        except Exception as e:
            print('Failed to load level:', e)

    @staticmethod
    def save(level, out):
        dos = DataOutputStream(out)
        dos.writeInt(LevelIO.MAGIC_NUMBER)
        dos.writeByte(LevelIO.CURRENT_VERSION)
        dos.write(pickle.dumps(level))
        dos.close()

    @staticmethod
    def loadBlocks(inp):
        dis = DataInputStream(inp)
        blocks = bytearray(dis.readInt())
        dis.readFully(blocks)
        dis.close()
        return blocks
