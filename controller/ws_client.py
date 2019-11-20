import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt5 import QtCore
import websocket


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'メインウィンドウ'
        self.width = 150
        self.height = 150
        self.initUI()
        self.thread = ListenWebsocket()
        self.thread.start()

    def initUI(self):
        self.setWindowTitle(self.title)

        btn1 = QPushButton("撮影", self)
        btn1.move(30, 50)
        # クリックされたらbuttonClickedの呼び出し
        btn1.clicked.connect(self.buttonClicked)

        self.show()

    def buttonClicked(self):
        # ステータスバーへメッセージの表示
        self.thread.WS.send("Hello")


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

    def on_message(ws, message):
        print("### message received ###")
        print(message)

    def on_error(ws, error):
        print(error)

    def on_close(ws):
        print("### closed ###")
        print(ws)


def main():
    app = QApplication(sys.argv)
    _ = MyWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
