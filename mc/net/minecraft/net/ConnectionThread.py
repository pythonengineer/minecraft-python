from mc.net.minecraft.comm.SocketConnection import SocketConnection
from mc.net.minecraft.gui.ErrorScreen import ErrorScreen
from mc.net.minecraft.net import Packets
from threading import Thread

class ConnectionThread(Thread):

    def __init__(self, connectionManager, ip, port, username, mpPass, minecraft):
        super().__init__()
        self.__connectionManager = connectionManager
        self.__ip = ip
        self.__port = port
        self.__username = username
        self.__mpPass = mpPass
        self.__minecraft = minecraft

    def run(self):
        try:
            connection = SocketConnection(self.__ip, self.__port)
            self.__connectionManager.connection = connection
            connection.manager = self.__connectionManager
            connection.sendPacket(Packets.LOGIN, [6, self.__username, self.__mpPass, 0])
            self.__connectionManager.processData = True
        except ConnectionRefusedError:
            self.__minecraft.hideGui = False
            self.__minecraft.connectionManager = None
            self.__minecraft.setScreen(ErrorScreen('Failed to connect', 'You failed to connect to the server. It\'s probably down!'))
            self.__connectionManager.processData = False
