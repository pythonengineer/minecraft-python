from mc.net.minecraft.comm.SocketConnection import SocketConnection
from mc.net.minecraft.net.ConnectionThread import ConnectionThread
from mc.net.minecraft.net import Packets
from mc.net.minecraft.gui.ErrorScreen import ErrorScreen
import traceback

class ConnectionManager:
    levelBuffer = None
    connection = None
    processData = False
    connected = False
    players = {}

    def __init__(self, minecraft, ip, port, username, mpPass):
        minecraft.hideGui = True
        self.minecraft = minecraft
        ConnectionThread(self, ip, port, username, mpPass, minecraft).start()

    def sendBlockChange(self, x, y, z, editMode, paintTexture):
        self.connection.sendPacket(Packets.PLACE_OR_REMOVE_TILE, [x, y, z, editMode, paintTexture])

    def disconnect(self, e):
        self.connection.disconnect()
        self.minecraft.setScreen(ErrorScreen('Disconnected!', str(e)))
        print(traceback.format_exc())

    def isConnected(self):
        return self.connection and self.connection.connected
