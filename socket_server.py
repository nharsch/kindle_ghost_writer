import asyncio
import json
import websockets
import logging
logger = logging.getLogger('websockets')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

clients = set()
# def handler()

async def update_all(html):
    for client in clients:
        await  client.send(json.dumps({'html':html}))

async def app(websocket, path):
    # register websocket
    print("registering new client", websocket)
    clients.add(websocket)
    async for message in websocket:
        html = json.loads(message)['html']
        print('updated html: ', html)
        await update_all(html)

asyncio.get_event_loop().run_until_complete(
    websockets.serve(app, '192.168.1.65', 8800))
asyncio.get_event_loop().run_forever()



# async def hello(uri):
#     async with websockets.connect(uri) as websocket:
#         await websocket.send("Hello world!")
#
# asyncio.get_event_loop().run_until_complete(
#     hello('ws://192.168.0.1:8800'))
