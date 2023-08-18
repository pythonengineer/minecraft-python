from enum import Enum

class DataTypes(Enum):
    Long = 0
    Integer = 1
    Short = 2
    Byte = 3
    Float = 4
    Double = 5
    Bytes = 6
    String = 7

class Packet:
    PACKETS = [None] * 256
    __nextId = 0

    def __init__(self, types):
        self.id = Packet.__nextId
        Packet.__nextId += 1
        Packet.PACKETS[self.id] = self
        self.fields = types
        size = 0

        for field in types:
            if field == DataTypes.Long:
                size += 8
            elif field == DataTypes.Integer:
                size += 4
            elif field == DataTypes.Short:
                size += 2
            elif field == DataTypes.Byte:
                size += 1
            elif field == DataTypes.Float:
                size += 4
            elif field == DataTypes.Double:
                size += 8
            elif field == DataTypes.Bytes:
                size += 1024
            elif field == DataTypes.String:
                size += 64

        self.size = size
