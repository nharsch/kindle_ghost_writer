# Kindle Ghost Writer

## Starting up

Start server:

```
pip isntall requirements.txt
python twisted_server.py
```

To type, go to `localhost:8888/typer`

To view, go to `localhost:8888/screen`


## Ok, but what about my kindle?

In order for the kindle to connect to your server, it will need
to be on the same network as the server, and you'll need to
replace `localhost` with the ip address of the server in `js/constants`.


## Considerations

The Kindle Experimental Browser does support websockets, but uses the
[`draft-76`](https://tools.ietf.org/html/draft-hixie-thewebsocketprotocol-76) 
protocol.
Because of that, I needed to use a websocket library that will handle the wierd 
`draft-76` style handshake.

## But why?
I wanted a distraction and glare free way to write, but didn't want 
to shell out the money for one of [these](https://getfreewrite.com/)

## TODO

- Unique channels/urls
- Ability to save/edit docs
- Find python3 websocket library that supports draft-75 protocol
