from websocket_server import WebsocketServer


CLIENTS = []


def new_client(client, server):
    print('New client {}:{} has joined.'.format(
        client['address'][0], client['address'][1]))

    CLIENTS.append(client)


def client_left(client, server):
    print('Client {}:{} has left.'.format(
        client['address'][0], client['address'][1]))

    CLIENTS.remove(client)
    # 接続台数が少ない場合音を鳴らす
    for c in CLIENTS:
        server.send_message(c, "stop")
    while len(CLIENTS) < 5:
        print("\007", end="")


def message_received(client, server, message):
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
    # controllerからの応答をraspiに返す
    else:
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
