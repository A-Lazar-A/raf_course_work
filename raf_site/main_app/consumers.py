# consumers.py

import cv2
import base64
import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer

class VideoStreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()

            # Обработка frame...

            _, buffer = cv2.imencode('.jpg', frame)
            data = base64.b64encode(buffer.tobytes()).decode('utf-8')

            await self.send(json.dumps({'image': data}))

            await asyncio.sleep(0.1)
