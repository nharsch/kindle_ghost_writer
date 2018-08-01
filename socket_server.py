#!/usr/bin/env python3

import asyncio
import json
import websockets
import logging
logger = logging.getLogger('websockets')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

global clients
clients = set()
# def handler()

# handshake for draft-76
def parse_headers (data):
    headers = {}
    lines = data.splitlines()
    for l in lines:
        parts = l.split(": ", 1)
        if len(parts) == 2:
            headers[parts[0]] = parts[1]
    headers['code'] = lines[len(lines) - 1]
    return headers

@asyncio.coroutine
def handshake (websocket):
    print('Handshaking...')
    data = yield from websocket.recv(1024)
    headers = parse_headers(data)
    print('Got headers:')
    for k, v in headers.iteritems():
        print(k, ':', v)
    if not headers.get('Sec-WebSocket-Key1'):
        return None
    digest = create_hash(
        headers['Sec-WebSocket-Key1'],
        headers['Sec-WebSocket-Key2'],
        headers['code']
    )
    shake = "HTTP/1.1 101 Web Socket Protocol Handshake\r\n"
    shake += "Upgrade: WebSocket\r\n" 
    shake += "Connection: Upgrade\r\n"
    shake += "Sec-WebSocket-Origin: %s\r\n" % (headers['Origin'])
    shake += "Sec-WebSocket-Location: ws://%s/stuff\r\n" % (headers['Host'])
    shake += "Sec-WebSocket-Protocol: sample\r\n\r\n"
    shake += digest
    yield from websocket.send(shake)


@asyncio.coroutine
def update_all(html):
    removed = set()
    global clients
    # remove closed clients
    clients = set(c for c in clients if not c.closed)
    for client in clients:
        if client.closed:
            removed.add(client)
        yield from client.send(json.dumps({'html':html}))


@asyncio.coroutine
def consumer(websocket, path):
    # register websocket
    handshake(websocket)
    clients.add(websocket)
    while True:
        message = yield from websocket.recv()
        print(message)
        if message[0] == "{":
            html = json.loads(message).get('html')
            if html:
                yield from update_all(html)

# @asyncio.coroutine
# def app(websocket, path):


asyncio.get_event_loop().run_until_complete(
    websockets.serve(consumer, '192.168.1.65', 8080))
asyncio.get_event_loop().run_forever()


# TODO: try consumer/producer pattern, with queue to save messages
# async def handler(websocket, path):
#     consumer_task = asyncio.ensure_future(
#         consumer_handler(websocket, path))
#     producer_task = asyncio.ensure_future(
#         producer_handler(websocket, path))
#     done, pending = await asyncio.wait(
#         [consumer_task, producer_task],
#         return_when=asyncio.FIRST_COMPLETED,
#     )
#     for task in pending:
#         task.cancel()



# async def hello(uri):
#     async with websockets.connect(uri) as websocket:
#         await websocket.send("Hello world!")
#
# asyncio.get_event_loop().run_until_complete(
#     hello('ws://192.168.0.1:8800'))
