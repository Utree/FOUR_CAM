import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLineEdit
from PyQt5 import QtCore
import websocket


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'メインウィンドウ'
        self.initUI()
        self.thread = ListenWebsocket()
        self.thread.start()

    def initUI(self):
        self.setWindowTitle(self.title)

        self.btn1 = QPushButton("撮影開始", self)
        self.btn1.setStyleSheet("background-color: #2190ff")
        self.btn1.move(30, 50)
        self.btn1.clicked.connect(self.startBtn)

        self.btn2 = QPushButton("撮影停止", self)
        self.btn2.setStyleSheet("background-color: #ff8121")
        self.btn2.move(200, 50)
        self.btn2.clicked.connect(self.stopBtn)

        self.btn3 = QPushButton("ラベル変更", self)
        self.btn3.setStyleSheet("background-color: #58d411")
        self.btn3.move(200, 100)
        self.btn3.clicked.connect(self.labelBtn)

        self.tb1 = QLineEdit(self)
        self.tb1.move(30, 110)
        self.tb1.resize(140, 20)

        self.btn4 = QPushButton("状態確認", self)
        self.btn4.setStyleSheet("background-color: #ffffff")
        self.btn4.move(30, 200)
        self.btn4.clicked.connect(self.checkBtn)

        self.show()

    def startBtn(self):
        self.thread.WS.send("start")

    def stopBtn(self):
        self.thread.WS.send("stop")

    def labelBtn(self):
        self.thread.WS.send(self.tb1.text())

    def checkBtn(self):
        self.thread.WS.send("status")


class ListenWebsocket(QtCore.QThread):
    def __init__(self, parent=None):
        super(ListenWebsocket, self).__init__(parent)

        websocket.enableTrace(True)

        self.WS = websocket.WebSocketApp("ws://127.0.0.1:8080/",
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)

    def run(self):
        self.WS.run_forever(http_proxy_host="")

    def on_message(self, message):
        print("### message received ###")
        print(message)

    def on_error(self, error):
        print(error)

    def on_close(self):
        print("### closed ###")


def main():
    width = 350
    height = 250
    app = QApplication(sys.argv)
    win = MyWindow()
    win.resize(width, height)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
