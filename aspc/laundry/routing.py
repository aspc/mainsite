from channels.routing import route

channel_routing = [
    route('websocket.receive', 'aspc.laundry.consumers.ws_echo'),
]