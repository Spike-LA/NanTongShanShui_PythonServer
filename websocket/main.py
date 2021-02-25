from bottle import get, run
from bottle_websocket import GeventWebSocketServer
from bottle_websocket import websocket
from websocket_class import Websocket


@get('/', apply=[websocket])
def chat(ws):
    ws_object = Websocket()
    ws_object.connect(ws)


run(host='0.0.0.0', port=90, server=GeventWebSocketServer)
