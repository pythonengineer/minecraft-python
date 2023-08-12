from mc.net.minecraft.comm.SocketConnection import SocketConnection
from mc.net.minecraft.net import Packets

class ConnectionManager:
    levelBuffer = None
    players = {}

    def __init__(self, minecraft, server, port, username):
        self.connection = SocketConnection(server, port)
        self.connection.manager = self
        self.connection.sendPacket(Packets.LOGIN, [3, username, '--'])
        self.minecraft = minecraft
        self.minecraft.beginLevelLoading('Connecting..')
        self.minecraft.hideGui = True

    def sendBlockChange(self, x, y, z, editMode, paintTexture):
        self.connection.sendPacket(Packets.PLACE_OR_REMOVE_TILE, [x, y, z, editMode, paintTexture])
