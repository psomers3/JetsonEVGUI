from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget, QMenu, QAction, QMenuBar
from .SpeedWidget import SpeedWidget
from .IMUWidget import IMUWidget
from .LidarWidget import LidarWidget
from .VideoWidget import VideoWidget
from .SLAMWidget import SLAMWidget

# if using windows... need the Bonjour service for this way of specifying the domain
ip = "localhost"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        layout_widget = QWidget()
        layout = QGridLayout()
        layout.setSpacing(0)

        layout_widget.setLayout(layout)
        self.setCentralWidget(layout_widget)

        menubar = self.menuBar()
        # menubar.setNativeMenuBar(False)
        connections = menubar.addMenu("Connections")
        reconnect = connections.addAction("Connect")
        reconnect.triggered.connect(self.open_sockets)
        disconnect = connections.addAction("Disconnect")
        disconnect.triggered.connect(self.close_sockets)
        # menubar.addMenu(connections)
        # self.setMenuBar(menubar)

        self.speed = SpeedWidget()
        self.imu = IMUWidget()
        self.lidar = LidarWidget()
        self.slam = SLAMWidget()
        self.slam.show()
        self.video = VideoWidget()
        self.video.show()

        layout.addWidget(self.speed, 0, 0, 2, 1)
        layout.addWidget(self.imu, 0, 1, 2, 1)
        layout.addWidget(self.lidar, 2, 0, 2, 1)
        layout.addWidget(self.video, 2, 1, 2, 1)

        self.show()
        self.open_sockets()

    def open_sockets(self):
        self.speed.connect(ip=ip, port=4020)
        self.speed.plot.plot_timer.start()
        self.imu.connect(ip=ip, port=5025)
        self.imu.accel.plot_timer.start()
        self.imu.gyro.plot_timer.start()
        self.imu.mag.plot_timer.start()

        self.lidar.connect(ip=ip, port=5026)
        self.lidar.plot.plot_timer.start()
        self.video.connect(ip=ip, port=5027)
        self.slam.connect(ip=ip, port=5028)

    def close_sockets(self):
        self.speed.socket.stop()
        self.speed.socket_thread.quit()
        self.speed.connected = False
        self.speed.plot.plot_timer.stop()

        self.imu.socket.stop()
        self.imu.socket_thread.quit()
        self.imu.connected = False
        self.imu.accel.plot_timer.stop()
        self.imu.gyro.plot_timer.stop()
        self.imu.mag.plot_timer.stop()

        self.video.socket.stop()
        self.video.socket_thread.quit()
        self.video.connected = False

        self.lidar.socket.stop()
        self.lidar.socket_thread.quit()
        self.lidar.connected = False

        self.slam.socket.stop()
        self.slam.socket_thread.quit()
        self.slam.connected = False

    def closeEvent(self, event):
        self.close_sockets()
        self.slam.close()
        QMainWindow.closeEvent(self, event)
