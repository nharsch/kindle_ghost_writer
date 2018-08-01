#!/usr/bin/env python

import json
import cyclone.escape
import cyclone.web
import cyclone.websocket
import os.path
import sys
from twisted.python import log
from twisted.internet import reactor



# serve template
class MainHandler(cyclone.web.RequestHandler):
    def get(self):
        self.render("index.html")


class Application(cyclone.web.Application):
    def __init__(self):
        settings = dict(
        #     cookie_secret="43oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
        #     template_path=os.path.join(os.path.dirname(__file__), "templates"),
            js_path=os.path.join(os.path.dirname(__file__), "js"),
            css_path=os.path.join(os.path.dirname(__file__), "css"),
        #     xsrf_cookies=True,
        #     autoescape=None,
        )
        print(settings["js_path"])

        handlers = [
            (r"/", MainHandler),
            (r"/echo", EchoSocketHandler),
            (r"/(.*\.js)", cyclone.web.StaticFileHandler,
                dict(path=settings['js_path'])),
            (r"/(.*\.css)", cyclone.web.StaticFileHandler,
                dict(path=settings['css_path'])),
        ]
        cyclone.web.Application.__init__(self, handlers)


global clients
clients = set()

class EchoSocketHandler(cyclone.websocket.WebSocketHandler):


    def connectionMade(self, *args, **kwargs):
        log.msg("ws opened", args or "no args", kwargs or "no kwargs")
        global clients
        clients.add(self)

    def connectionLost(self, reason):
        log.msg("ws closed")

    def messageReceived(self, message):
        log.msg("got message %s" % message)
        self.sendMessage(message)
        if message[0] == "{":
            html = json.loads(message).get('html')
            if html:
                self.update_all(html)

    def close(self):
        global clients
        clients -= self

    def update_all(self, html):
        # remove closed clients
        global clients
        for client in clients:
            client.sendMessage(json.dumps({'html':html}))


def main():
    reactor.listenTCP(8888, Application())
    reactor.run()


if __name__ == "__main__":
    log.startLogging(sys.stdout)
    main()
