# consumers.py
import os

import cv2
import base64
import json
import asyncio

from channels.db import database_sync_to_async
from django.conf import settings
from django.core.asgi import get_asgi_application

# Настройка окружения Django


from django.core.serializers import serialize
import face_recognition
from channels.generic.websocket import AsyncWebsocketConsumer

from PIL import Image
from io import BytesIO
import logging

from django.shortcuts import get_object_or_404

from .face_rec import webcam_face_recognition_byFrame

# Настройка логирования
logger = logging.getLogger(__name__)


class VideoStreamConsumer1(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.user = None
        self.known_faces = []
        self.known_face_names = []
        for filename in os.listdir('registered_faces'):
            image_path = os.path.join('registered_faces', filename)
            img = face_recognition.load_image_file(image_path)
            encoding = face_recognition.face_encodings(img)[0]
            self.known_faces.append(encoding)
            self.known_face_names.append(os.path.splitext(filename)[0])
        # Открываем две камеры (можете добавить больше, если нужно)
        self.cap1 = cv2.VideoCapture(0)

        await self.send_images()

    async def disconnect(self, close_code):
        # Закрываем камеры при разрыве соединения
        self.cap1.release()

    @database_sync_to_async
    def get_user_data_by_id(self, face_id):
        from .models import User
        try:
            user = User.objects.get(id=face_id)
            user_data = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                # Добавьте остальные поля пользователя, которые вам нужны
            }
            return user_data
        except User.DoesNotExist:
            return None

    async def send_images(self):
        while True:
            ret1, frame1 = self.cap1.read()
            face_id1 = webcam_face_recognition_byFrame(frame1, self.known_faces, self.known_face_names)
            if face_id1:
                #     pass
                #     self.user = serialize('json', [await self.get_user_by_face_id(face_id1)])
                self.user = await self.get_user_data_by_id(face_id1)
            # Обработка frame1 и frame2...

            _, buffer1 = cv2.imencode('.jpg', frame1)

            data1 = base64.b64encode(buffer1.tobytes()).decode('utf-8')

            await self.send(json.dumps({'face_recognized': self.user, 'image1': data1}))

            await asyncio.sleep(0.1)


class VideoStreamConsumer2(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        # Открываем две камеры (можете добавить больше, если нужно)

        self.cap2 = cv2.VideoCapture(2)
        await self.send_images()

    async def disconnect(self, close_code):
        # Закрываем камеры при разрыве соединения

        self.cap2.release()

    def is_valid_jpeg(self, data):
        try:
            # Попытка открыть изображение с использованием Pillow
            img = Image.open(BytesIO(base64.b64decode(data)))
            img.verify()
            img.close()
            return True
        except Exception as e:
            logger.warning(f"Invalid JPEG data: {e}")
            return False

    async def send_images(self):
        while True:

            ret2, frame2 = self.cap2.read()

            # Обработка frame1 и frame2...

            _, buffer2 = cv2.imencode('.jpg', frame2)

            data2 = base64.b64encode(buffer2.tobytes()).decode('utf-8')

            # Проверка данных перед отправкой
            if not all([self.is_valid_jpeg(data2)]):
                continue

            await self.send(json.dumps({'image2': data2}))

            await asyncio.sleep(0.1)
