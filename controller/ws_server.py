from websocket_server import WebsocketServer
from pydub import AudioSegment
from pydub.playback import play

change_audio = AudioSegment.from_mp3('./change.mp3')
restart_audio = AudioSegment.from_mp3('./restart.mp3')
rotate_audio = AudioSegment.from_mp3('./rotate.mp3')

CLIENTS = []
shooting = False
RASPI_NUM = 4
SHOT_NUM = 12
ok_counter = 0
shot_counter = 0


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
    global RASPI_NUM, SHOT_NUM, ok_counter, shot_counter, shooting

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
                play(change_audio)
            else:
                play(rotate_audio)
    # controllerからの応答をraspiに返す
    else:
        if message == "start":
            shooting = True
        elif message == "stop":
            ok_counter = 0
            shot_counter = 0
            shooting = False
        for c in CLIENTS:
            if c != client:
                server.send_message(c, reply_message)
                print('Message "{}" has been sent to {}:{}'.format(
                    reply_message, c['address'][0], c['address'][1]))


# Main
if __name__ == "__main__":
    server = WebsocketServer(port=8080, host='0.0.0.0')
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.set_fn_message_received(message_received)
    server.run_forever()
