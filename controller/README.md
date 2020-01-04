# 使い方

```
# 必要ソフトをインストール
$ brew install portaudio
$ pip install pyqt5 pyaudio pydub
$ pip install websocket-client==0.47.0
$ pip install pip install git+https://github.com/Pithikos/python-websocket-server

# サーバーを起動
$ python ws_server.py
# コントローラを起動
$ python ws_client.py

# コントローラ側のIPアドレスをraspi側の4cam_cv3.pyファイル
# 36行目
# IP = "192.168.1.69"
# に指定
```
