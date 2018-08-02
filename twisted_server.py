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
class TyperHandler(cyclone.web.RequestHandler):
    def get(self):
        self.render("type_index.html")


class ScreenHandler(cyclone.web.RequestHandler):
    def get(self):
        self.render("screen_index.html")


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
            (r"/screen", ScreenHandler),
            (r"/typer", TyperHandler),
            (r"/typer_socket", TyperSocketHandler),
            (r"/screen_socket", ScreenSocketHandler),
            (r"/(.*\.js)", cyclone.web.StaticFileHandler,
                dict(path=settings['js_path'])),
            (r"/(.*\.css)", cyclone.web.StaticFileHandler,
                dict(path=settings['css_path'])),
        ]
        cyclone.web.Application.__init__(self, handlers)


global clients
screen_clients = set()

class BaseSocketHandler(cyclone.websocket.WebSocketHandler):

    def connectionMade(self, *args, **kwargs):
        log.msg("ws opened", args or "no args", kwargs or "no kwargs")

    def connectionLost(self, reason):
        log.msg("ws closed")


class TyperSocketHandler(BaseSocketHandler):

    def messageReceived(self, message):
        log.msg("got message %s" % message)
        if message[0] == "{":
            html = json.loads(message).get('html')
            self.update_all(html)

    def update_all(self, html):
        # remove closed clients
        global screen_clients
        for client in screen_clients:
            client.sendMessage(json.dumps({'html':html}))


class ScreenSocketHandler(BaseSocketHandler):

    def connectionMade(self, *args, **kwargs):
        log.msg("ws opened", args or "no args", kwargs or "no kwargs")
        global screen_clients
        screen_clients.add(self)

    def close(self):
        global screen_clients
        screen_clients -= self


def main():
    reactor.listenTCP(8888, Application())
    reactor.run()


if __name__ == "__main__":
    log.startLogging(sys.stdout)
    main()
