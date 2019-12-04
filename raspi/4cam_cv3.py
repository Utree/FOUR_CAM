#!/usr/bin/python

import os
import sys
import time
import RPi.GPIO as gp
from PyQt5 import QtCore, QtGui, QtWidgets
import setup_qt_ui
import gui_ui
import cv2
import subprocess
import datetime
import websocket

######################################
'''
画像のパラメータ
'''
width = 240  # 320
height = 320  # 240
fps = 30
brightness = 50               # min=0   max=100  step=1
contrast = 0                  # min=-100  max=100  step=1
saturation = 0                # min=-100  max=100  step=1
rotate = 0                    # min=0  max=360  step=90
auto_exposure = 0             # min=0  max=3
exposure_time_absolute = 1000  # min = 1  max=10000  step=1
'''
撮影方法のパラメータ
'''
# 秒間のインターバル
interval = 3
# 保存場所
storage = "/home/pi/Desktop/4cam_img/"
# 指示機のIPアドレス
IP = "192.168.1.251"
# 指示機のポート番号
PORT = "8080"

'''
その他の変数
'''
# 現在時刻
previous_time = datetime.datetime.now()
# 撮影中フラグ
take_photo_flag = False
# 画面に表示中の画像
ui_label_img_list = []
#######################################

gp.setwarnings(False)
gp.setmode(gp.BOARD)
gp.setup(7, gp.OUT)
gp.setup(11, gp.OUT)
gp.setup(12, gp.OUT)


class PhotoGrabThread(QtCore.QThread):
    grabbed_signal = QtCore.pyqtSignal([int, QtGui.QImage])

    def __init__(self, p):
        super(PhotoGrabThread, self).__init__()
        self.index = 0
        self.index_top = p.img_no

    def run(self):

        i2c = "i2cset -y 1 0x70 0x00 0x04"
        os.system(i2c)
        gp.output(7, False)
        gp.output(11, False)
        gp.output(12, True)

        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, width)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, height)
        cap.set(cv2.CAP_PROP_FPS, fps)
        command = "v4l2-ctl -d 0 -c brightness=%d" % (brightness)
        _ = subprocess.call(command, shell=True)
        command = "v4l2-ctl -d 0 -c contrast=%d" % (contrast)
        _ = subprocess.call(command, shell=True)
        command = "v4l2-ctl -d 0 -c saturation=%d" % (saturation)
        _ = subprocess.call(command, shell=True)
        command = "v4l2-ctl -d 0 -c rotate=%d" % (rotate)
        _ = subprocess.call(command, shell=True)
        command = "v4l2-ctl -d 0 -c auto_exposure=%d" % (auto_exposure)
        _ = subprocess.call(command, shell=True)
        command = "v4l2-ctl -d 0 -c exposure_time_absolute=%d" % (
            exposure_time_absolute)
        _ = subprocess.call(command, shell=True)
        rev, frame = cap.read()
        time.sleep(1)
        i2c = "i2cset -y 1 0x70 0x00 0x05"
        os.system(i2c)
        gp.output(7, True)
        gp.output(11, False)
        gp.output(12, True)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, width)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, height)
        cap.set(cv2.CAP_PROP_FPS, fps)
        command = "v4l2-ctl -d 0 -c brightness=%d" % (brightness)
        _ = subprocess.call(command, shell=True)
        command = "v4l2-ctl -d 0 -c contrast=%d" % (contrast)
        _ = subprocess.call(command, shell=True)
        command = "v4l2-ctl -d 0 -c saturation=%d" % (saturation)
        _ = subprocess.call(command, shell=True)
        command = "v4l2-ctl -d 0 -c rotate=%d" % (rotate)
        _ = subprocess.call(command, shell=True)
        command = "v4l2-ctl -d 0 -c auto_exposure=%d" % (auto_exposure)
        _ = subprocess.call(command, shell=True)
        command = "v4l2-ctl -d 0 -c exposure_time_absolute=%d" % (
            exposure_time_absolute)
        _ = subprocess.call(command, shell=True)
        rev, frame = cap.read()
        time.sleep(1)
        i2c = "i2cset -y 1 0x70 0x00 0x06"
        os.system(i2c)
        gp.output(7, False)
        gp.output(11, True)
        gp.output(12, False)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, width)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, height)
        cap.set(cv2.CAP_PROP_FPS, fps)
        command = "v4l2-ctl -d 0 -c brightness=%d" % (brightness)
        _ = subprocess.call(command, shell=True)
        command = "v4l2-ctl -d 0 -c contrast=%d" % (contrast)
        _ = subprocess.call(command, shell=True)
        command = "v4l2-ctl -d 0 -c saturation=%d" % (saturation)
        _ = subprocess.call(command, shell=True)
        command = "v4l2-ctl -d 0 -c rotate=%d" % (rotate)
        _ = subprocess.call(command, shell=True)
        command = "v4l2-ctl -d 0 -c auto_exposure=%d" % (auto_exposure)
        _ = subprocess.call(command, shell=True)
        command = "v4l2-ctl -d 0 -c exposure_time_absolute=%d" % (
            exposure_time_absolute)
        _ = subprocess.call(command, shell=True)
        rev, frame = cap.read()

        time.sleep(1)
        i2c = "i2cset -y 1 0x70 0x00 0x07"
        os.system(i2c)
        gp.output(7, True)
        gp.output(11, True)
        gp.output(12, False)
        rev, frame = cap.read()
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, width)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, height)
        cap.set(cv2.CAP_PROP_FPS, fps)
        command = "v4l2-ctl -d 0 -c brightness=%d" % (brightness)
        _ = subprocess.call(command, shell=True)
        command = "v4l2-ctl -d 0 -c contrast=%d" % (contrast)
        _ = subprocess.call(command, shell=True)
        command = "v4l2-ctl -d 0 -c saturation=%d" % (saturation)
        _ = subprocess.call(command, shell=True)
        command = "v4l2-ctl -d 0 -c rotate=%d" % (rotate)
        _ = subprocess.call(command, shell=True)
        command = "v4l2-ctl -d 0 -c auto_exposure=%d" % (auto_exposure)
        _ = subprocess.call(command, shell=True)
        command = "v4l2-ctl -d 0 -c exposure_time_absolute=%d" % (
            exposure_time_absolute)
        _ = subprocess.call(command, shell=True)
        time.sleep(1)

        index = 0
        while 1:
            rev, frame = cap.read()
            rev, frame = cap.read()
            rev, frame = cap.read()
            if index == 0:
                gp.output(7, False)
                gp.output(11, False)
                gp.output(12, True)
            if index == 3:
                gp.output(7, True)
                gp.output(11, False)
                gp.output(12, True)
            if index == 1:
                gp.output(7, False)
                gp.output(11, True)
                gp.output(12, False)
            if index == 2:
                gp.output(7, True)
                gp.output(11, True)
                gp.output(12, False)

            h, w, c = frame.shape
            bytes_per_line = 3 * w
            f_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            qimg = QtGui.QImage(
                f_rgb.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)

            self.grabbed_signal.emit(index, qimg)

            index += 1
            index %= self.index_top


class ListenWebsocket(QtCore.QThread):
    """Webソケットのクライアントスレッド

    Websocketのクライアントとして挙動
    メッセージ受信時に写真を保存
    画像の名前は[タイムスタンプ_カメラID.png]。
    """
    def __init__(self, parent=None):
        global IP, PORT

        super(ListenWebsocket, self).__init__(parent)

        websocket.enableTrace(True)

        self.WS = websocket.WebSocketApp("ws://" + IP + ":" + PORT + "/",
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)

    def run(self):
        self.WS.run_forever()

    def on_message(self, ws, message):
        global take_photo_flag, previous_time

        print("### message received ###")
        print(message)

        # 現在時刻
        previous_time = datetime.datetime.now()

        if take_photo_flag:
            take_photo_flag = False
        else:
            take_photo_flag = True

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        print("### closed ###")


class CamGui(QtWidgets.QMainWindow):

    def __init__(self, *args):
        global ui_label_img_list

        super(CamGui, self).__init__(*args)
        self.ui = gui_ui.Ui_MainWindow()
        self.ui.setupUi(self)
        ui_label_img_list = [
            self.ui.label_img0, self.ui.label_img1,
            self.ui.label_img2, self.ui.label_img3
        ]
        self.img_no = len(ui_label_img_list)

        # マウスクリックのイベント
        self.ui.label_img0.mouseReleaseEvent = self.on_mouse_release_label_img

        # Webosocket スレッド
        self.ws_thread = ListenWebsocket()
        self.ws_thread.start()

        # camera スレッド
        self.grab_thread = PhotoGrabThread(self)
        self.grab_thread.grabbed_signal.connect(self.update_photo)
        self.grab_thread.start()

    def update_photo(self, index, qimg):
        """定周期で撮影する用の関数

        グローバル変数のinterval(秒)間隔で表示されている画像をpngファイルとして
        保存する関数。
        撮影開始のトリガはメインウィンドウ左上の画像押下。
        画像の名前は[タイムスタンプ_カメラID.png]。
        """
        global previous_time, ui_label_img_list

        ui_label_img_list[index].setPixmap(QtGui.QPixmap.fromImage(qimg))

        # 現在時刻を取得
        dt = datetime.datetime.now()

        if take_photo_flag and (dt-previous_time).seconds > interval:
            # 画像を保存
            for i in range(len(ui_label_img_list)):
                ui_label_img_list[i].pixmap().save(
                    storage + str(dt) + "_" + str(i) + ".png")
            # 時間を更新
            previous_time = dt

    def on_mouse_release_label_img(self, ev):
        """メインウィンドウの押下処理

        メインウィンドウ左上の画像押下時にグローバル変数take_photo_flagを立てる
        """
        global take_photo_flag

        if take_photo_flag:
            take_photo_flag = False
        else:
            take_photo_flag = True


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = CamGui()
    gui.show()
    sys.exit(app.exec_())
