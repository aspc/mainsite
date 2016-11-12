from channels.routing import route

channel_routing = [
    route('websocket.connect', 'aspc.laundry.consumers.machine_details', path=r'^/laundry/machine/(?P<pk>\w+)/$'), #(?P<pk>\w+)
    route('websocket.receive', 'aspc.laundry.consumers.process_stream'),
]