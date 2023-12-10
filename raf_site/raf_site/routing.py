# routing.py

from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from main_app import consumers

application = ProtocolTypeRouter({
    'websocket': URLRouter([
        path('ws/video_stream/', consumers.VideoStreamConsumer.as_asgi()),
    ]),
})
