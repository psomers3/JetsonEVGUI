from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import QThread
from GUI.QDataSocket import QDataSocket
from .plotTypes import SLAMPlot


class SLAMWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.plot = SLAMPlot(label="SLAM")
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.plot)
        self.layout().setSpacing(0)
        self.connected = False

    def connect(self, port, ip="localhost"):
        if self.connected:
            return
        self.socket = QDataSocket(tcp_ip=ip, tcp_port=port)
        self.socket_thread = QThread()
        self.socket.moveToThread(self.socket_thread)
        self.socket_thread.started.connect(self.socket.start)
        self.socket.new_data.connect(self.plot.update_plot)
        self.socket_thread.start()
        self.connected = True
