from os.path import join, dirname
from websocket_server import WebsocketServer
from pydub import AudioSegment
from pydub.playback import play
from os.path import exists
from switch import main as rotate
from time import sleep

connect_drive_audio = AudioSegment.from_mp3(join(dirname(__file__), 'connect_drive.mp3'))
change_audio = AudioSegment.from_mp3(join(dirname(__file__), 'change.mp3'))
restart_audio = AudioSegment.from_mp3(join(dirname(__file__), 'restart.mp3'))
rotate_audio = AudioSegment.from_mp3(join(dirname(__file__), 'rotate.mp3'))

CLIENTS = []
shooting = False
RASPI_NUM = 4
SHOT_NUM = 8
SCHEDULE = [36, 18, 36, 9, 36, 18, 36]
CHANGE_TIME = 6
WAIT_TIME = 3
ok_counter = 0
shot_counter = 0
drive_path = "/Volumes/Extreme SSD/scp/"


def new_client(client, server):
    print('New client {}:{} has joined.'.format(
        client['address'][0], client['address'][1]))

    CLIENTS.append(client)


def client_left(client, server):
    global restart_audio
    print('Client {}:{} has left.'.format(
        client['address'][0], client['address'][1]))

    CLIENTS.remove(client)
    # 接続台数が少ない場合音を鳴らす
    for c in CLIENTS:
        server.send_message(c, "stop")
    if len(CLIENTS) < 5:
        play(restart_audio)


def message_received(client, server, message):
    global RASPI_NUM, SHOT_NUM, ok_counter, shot_counter, shooting, SCHEDULE, CHANGE_TIME, WAIT_TIME

    print('Message "{}" has been received from {}:{}'.format(
        message, client['address'][0], client['address'][1]))
    reply_message = message

    # raspiからの応答をcontrollerに返す
    if message[:4] == "flag":
        for c in CLIENTS:
            if c['address'][0] == "127.0.0.1":
                server.send_message(c, reply_message)
                print('Message "{}" has been sent to {}:{}'.format(
                    reply_message, c['address'][0], c['address'][1]))
    elif message == "OK":
        print("ok_counter: " + str(ok_counter) + ", shot_counter: " + str(shot_counter))
        ok_counter = (ok_counter + 1) % RASPI_NUM

        if ok_counter == 0:
            shot_counter = (shot_counter + 1) % SHOT_NUM
            if shot_counter == 0:
                # 入れ替える
                play(change_audio)
                sleep(CHANGE_TIME)
            else:
                # 回転させる
                play(rotate_audio)
                rotate("On")
                sleep(SCHEDULE[shot_counter-1])
                rotate("Off")
            sleep(WAIT_TIME)

            # 次の撮影命令を出す
            if shooting:
                for c in CLIENTS:
                    if c['address'][0] != "127.0.0.1":
                        server.send_message(c, "shot")
    # controllerからの応答をraspiに返す
    else:
        """ START MESSAGE"""
        if message == "start":
            shooting = True
        elif message == "stop":
            ok_counter = 0
            shot_counter = 0
            shooting = False
            rotate("Off")
        for c in CLIENTS:
            if c != client:
                server.send_message(c, reply_message)
                print('Message "{}" has been sent to {}:{}'.format(
                    reply_message, c['address'][0], c['address'][1]))


# Main
if __name__ == "__main__":
    # 外部ディスクの接続確認
    if not exists(drive_path):
        play(connect_drive_audio)
    server = WebsocketServer(port=8080, host='0.0.0.0')
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.set_fn_message_received(message_received)
    server.run_forever()
