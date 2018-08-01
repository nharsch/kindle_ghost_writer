#!/usr/bin/env python3

import asyncio
import json
from os import path
from itertools import cycle

# TODO: req.txt
import websockets
from ansi2html import Ansi2HTMLConverter

conv = Ansi2HTMLConverter()


# TODO: open file for tailing
file_path = "log.txt"

def content_to_html(content):
    message = json.dumps({
        "html": conv.convert(content),
    })
    return message

@asyncio.coroutine
def view_log(websocket, url_path):
    print('new connection', websocket)
    loop = asyncio.get_running_loop()
    end_time = loop.time() + 5.0
    while True:
        if (loop.time() + 1.0) >= end_time:
            break
        else:
            with open(path.abspath(file_path)) as f:
                content = f.read()
                if content:
                    message = json.dumps({
                        "html": conv.convert(content),
                    })
                    yield from websocket.send(message)
                else:
                    yield from asyncio.sleep(1)

start_server = websockets.serve(view_log, '192.168.1.65', 8080)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
