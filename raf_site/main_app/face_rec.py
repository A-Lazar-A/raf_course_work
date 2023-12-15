import cv2
import dlib
import os
from datetime import datetime, timedelta
import threading
import time

import face_recognition


# import face_recognition


def register_faces_by_web(user_id):
    print('strat rec')

    def process_frames():
        nonlocal photo_count

        while photo_count < 3 and (datetime.now() - start_time) < timedelta(seconds=10):
            ret, frame = cap.read()

            if not ret:
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = detector(gray)

            for i, face in enumerate(faces):
                x, y, w, h = (face.left(), face.top(), face.width(), face.height())

                filename = f'./registered_faces/{user_id}_{photo_count}.jpg'
                cv2.imwrite(filename, frame[y:y + h, x:x + w])

                print(f'Face registered! Image saved as {filename}')

                photo_count += 1

                time.sleep(delay_between_shots)

        cap.release()
        cv2.destroyAllWindows()

    cap = cv2.VideoCapture(0)
    detector = dlib.get_frontal_face_detector()

    if not os.path.exists('registered_faces'):
        os.makedirs('registered_faces')

    start_time = datetime.now()
    photo_count = 0
    delay_between_shots = 3

    processing_thread = threading.Thread(target=process_frames)
    processing_thread.start()

    processing_thread.join()


def webcam_face_recognition_byFrame(frame, known_faces, known_face_names):
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_faces, face_encoding)

        # тут начинается проврерка на совпадение лица из базы
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            # костыль, чтобы пользователя не опозновало 100500 раз, наврено здесь вместо списка будет сверка с бд воше пользоваетль или нет
            worker = name.split("_")[0]

            # print(f"Match found: {worker}")

            return worker
