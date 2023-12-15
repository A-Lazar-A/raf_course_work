# routing.py

from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from main_app import consumers

application = ProtocolTypeRouter({
    'websocket': URLRouter([
        path('ws/video_stream1/', consumers.VideoStreamConsumer1.as_asgi()),
        path('ws/video_stream2/', consumers.VideoStreamConsumer2.as_asgi()),
    ]),
})
