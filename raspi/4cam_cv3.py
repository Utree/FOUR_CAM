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
from evacuate import evacuate

######################################
'''
画像のパラメータ
'''
'''
camera resolution
https://www.arducam.com/product/b003301-arducam-5mp-ov5647-1080p-noir-camera-for-raspberry-pi-infrared-camera-module-sensitive-to-ir-light/
https://stackoverflow.com/questions/19448078/python-opencv-access-webcam-maximum-resolution/20120262
'''
width = 1024
height = 1280
fps = 30
brightness = 50               # min=0   max=100  step=1
contrast = 0                  # min=-100  max=100  step=1
saturation = 0                # min=-100  max=100  step=1
rotate = 0                    # min=0  max=360  step=90
auto_exposure = 1             # exposure: manual
exposure_time_absolute = 60   # shutter time
auto_exposure_bias = 12       # exposure fix
white_balance_auto_preset = 0  # auto white balance setting
red_balance = 1500            # red balance vs green
blue_balance = 1000           # blue balance vs green
iso_sensitivity_auto = 0      # manual
iso_sensitivity = 1           # iso 100
'''
撮影方法のパラメータ
'''
# インターバル (n秒)
INTERVAL_TIME = 10
# 休憩時間 (n秒)
REST_TIME = 10
# 撮影回数 (n回)
SHOTS = 12
shot_counter = 0
# ラベル
label = "undefined"
# 保存場所
storage = "/home/pi/Desktop/4cam_img/"
PATH = storage
dir_name = ""
# 指示機のIPアドレス
IP = "192.168.1.110"
# 指示機のポート番号
PORT = "8080"

'''
その他の変数
'''
# 次の撮影時間
next_shot_time = datetime.datetime.now()
# 撮影中フラグ
take_photo_flag = False
# 画像
IMGS = [None, None, None, None]
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
        command = "v4l2-ctl -d 0 -c auto_exposure=%d,exposure_time_absolute=%d,auto_exposure_bias=%d" % (
            auto_exposure, exposure_time_absolute, auto_exposure_bias)
        _ = subprocess.call(command, shell=True)
        command = "v4l2-ctl -d 0 -c white_balance_auto_preset=%d,red_balance=%d,blue_balance=%d" % (
            white_balance_auto_preset, red_balance, blue_balance)
        _ = subprocess.call(command, shell=True)
        command = "v4l2-ctl -d 0 -c iso_sensitivity_auto=%d,iso_sensitivity=%d" % (
            iso_sensitivity_auto, iso_sensitivity)
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
        command = "v4l2-ctl -d 0 -c auto_exposure=%d,exposure_time_absolute=%d,auto_exposure_bias=%d" % (
            auto_exposure, exposure_time_absolute, auto_exposure_bias)
        _ = subprocess.call(command, shell=True)
        command = "v4l2-ctl -d 0 -c white_balance_auto_preset=%d,red_balance=%d,blue_balance=%d" % (
            white_balance_auto_preset, red_balance, blue_balance)
        _ = subprocess.call(command, shell=True)
        command = "v4l2-ctl -d 0 -c iso_sensitivity_auto=%d,iso_sensitivity=%d" % (
            iso_sensitivity_auto, iso_sensitivity)
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
        command = "v4l2-ctl -d 0 -c auto_exposure=%d,exposure_time_absolute=%d,auto_exposure_bias=%d" % (
            auto_exposure, exposure_time_absolute, auto_exposure_bias)
        _ = subprocess.call(command, shell=True)
        command = "v4l2-ctl -d 0 -c white_balance_auto_preset=%d,red_balance=%d,blue_balance=%d" % (
            white_balance_auto_preset, red_balance, blue_balance)
        _ = subprocess.call(command, shell=True)
        command = "v4l2-ctl -d 0 -c iso_sensitivity_auto=%d,iso_sensitivity=%d" % (
            iso_sensitivity_auto, iso_sensitivity)
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
        command = "v4l2-ctl -d 0 -c auto_exposure=%d,exposure_time_absolute=%d,auto_exposure_bias=%d" % (
            auto_exposure, exposure_time_absolute, auto_exposure_bias)
        _ = subprocess.call(command, shell=True)
        command = "v4l2-ctl -d 0 -c white_balance_auto_preset=%d,red_balance=%d,blue_balance=%d" % (
            white_balance_auto_preset, red_balance, blue_balance)
        _ = subprocess.call(command, shell=True)
        command = "v4l2-ctl -d 0 -c iso_sensitivity_auto=%d,iso_sensitivity=%d" % (
            iso_sensitivity_auto, iso_sensitivity)
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

            IMGS[index] = f_rgb

            qimg = QtGui.QImage(
                f_rgb.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)

            self.grabbed_signal.emit(index, qimg)

            index += 1
            index %= self.index_top


class ListenWebsocket(QtCore.QThread):
    """Webソケットのクライアントスレッド.

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
        global take_photo_flag, label, PATH, storage, next_shot_time, shot_counter, dir_name

        print("### message received ###")
        print(message)

        # messageがstartのとき撮影開始
        if message == "start":
            # ディレクトリをつくる
            now = datetime.datetime.now()
            os.makedirs(
                storage + "/" +
                now.strftime("%Y-%m-%d_%H-%M-%S")
            )
            shot_counter = 0
            PATH = storage + "/" + now.strftime("%Y-%m-%d_%H-%M-%S") + "/"
            dir_name = now.strftime("%Y-%m-%d_%H-%M-%S")
            next_shot_time = now
            take_photo_flag = True
        # messageがstopのとき撮影停止
        elif message == "stop":
            take_photo_flag = False
            # データ退避
            if not dir_name == "":
                evacuate(dir_name)
        # messageがstatusのとき現在の情報を提示
        elif message == "status":
            status = "flag: " + str(take_photo_flag) + ",Dir: " + PATH + ",nextshot: " + next_shot_time.strftime(
                "%Y-%m-%d_%H-%M-%S") + ",prevangle: " + str(shot_counter) + ",label: " + label
            ws.send(status)
        # messageがその他のときラベル更新
        else:
            label = message

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        print("### closed ###")


class CamGui(QtWidgets.QMainWindow):

    def __init__(self, *args):
        super(CamGui, self).__init__(*args)
        self.ui = gui_ui.Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui_label_img_list = [
            self.ui.label_img0, self.ui.label_img1,
            self.ui.label_img2, self.ui.label_img3
        ]
        self.img_no = len(self.ui_label_img_list)

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
        """定周期で撮影する用の関数.

        グローバル変数のINTERVAL_TIME(秒)間隔で表示されている画像をpngファイルとして
        保存する関数。
        撮影開始のトリガはメインウィンドウ左上の画像押下。
        画像の名前は[タイムスタンプ_カメラID_angelID_label.png]。
        """
        global INTERVAL_TIME, REST_TIME, shot_counter, SHOTS, label, PATH, next_shot_time, IMGS

        self.ui_label_img_list[index].setPixmap(QtGui.QPixmap.fromImage(qimg))

        # 現在時刻を取得
        now = datetime.datetime.now()
        if take_photo_flag:
            # 予定された撮影時間より過ぎていたとき
            if next_shot_time <= now:
                # 画像を保存
                for index, value in enumerate(IMGS):
                    cv2.imwrite(PATH + now.strftime("%Y-%m-%d_%H-%M-%S")
                                + "_cam" + str(index)
                                + "_angle" + str(shot_counter)
                                + "_" + label + ".png",
                                cv2.cvtColor(value, cv2.COLOR_BGR2RGB))
                # shot_counterを更新
                shot_counter = (shot_counter + 1) % SHOTS
                # 時間を更新
                if shot_counter != 0:
                    next_shot_time = next_shot_time + \
                        datetime.timedelta(seconds=INTERVAL_TIME)
                else:
                    next_shot_time = next_shot_time + \
                        datetime.timedelta(seconds=REST_TIME)
                # 撮影終了をcontorllerに知らせる
                self.ws_thread.WS.send("OK")

    def on_mouse_release_label_img(self, ev):
        """メインウィンドウの押下処理.

        メインウィンドウ左上の画像押下時に撮影する
        """
        global shot_counter, label, PATH, next_shot_time, IMGS

        # 現在時刻を取得
        now = datetime.datetime.now()
        for index, value in enumerate(IMGS):
            cv2.imwrite(PATH + now.strftime("%Y-%m-%d_%H-%M-%S")
                        + "_cam" + str(index)
                        + "_angle" + str(shot_counter)
                        + "_" + label + ".png",
                        cv2.cvtColor(value, cv2.COLOR_BGR2RGB))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = CamGui()
    gui.show()
    sys.exit(app.exec_())
