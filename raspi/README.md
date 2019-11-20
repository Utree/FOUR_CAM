# 使い方

```
$ cd ~
# pyqtをインストール
$ sudo apt-get install python-pyqt5

# opencvインストール用にraspiのスワップサイズを変更
# /etc/dphys-swapfileで
# CONF_SWAPSIZE=2048
# に変更
$ sudo systemctl stop dphys-swapfile
$ sudo systemctl start dphys-swapfile

# opencvの最新バージョンをインストール
$ python3.7 -m pip install numpy
$ sudo apt-get update -y && sudo apt-get install -y --no-install-recommends \
build-essential cmake git libgtk2.0-dev pkg-config libavcodec-dev \
libavformat-dev libswscale-dev python-dev python-numpy libtbb2 \
libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev
$ git clone https://github.com/opencv/opencv.git && \
$ git clone https://github.com/opencv/opencv_contrib.git
$ mkdir -p ./opencv/build/
$ cd ./opencv/build/
$ cmake -DOPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \
-D PYTHON3_EXECUTABLE=$(which python3.7) \
-D PYTHON3_NUMPY_INCLUDE_DIRS=$(python3.7 -c "import numpy;print(numpy.get_include())") \
-DPYTHON_DEFAULT_EXECUTABLE=$(which python3.7) \
-D CMAKE_BUILD_TYPE=Release -D CMAKE_INSTALL_PREFIX=/usr/local .. && \
sudo make && sudo make install
$ cd
$ rm -rf ./opencv
$ rm -rf ./opencv_contrib

# raspi-configでcameraとi2cを有効にして、再起動

# websocket-clientをインストール
$ python3 -m pip install websocket-client==0.47.0

# ソースコードをダウンロード
$ cd ~/Desktop
$ git clone https://github.com/Utree/RaspberryPi.git

# カメラを利用
$ cd Desktop/RaspberryPi/Multi_Camera_Adapter/Multi_Adapter_Board_4Channel/Multi_Camera_Adapter_V2.1
$ chmod +x ./init_camera.sh
$ python3 4cam_cv3.py
```
