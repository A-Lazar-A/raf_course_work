import cv2
import dlib
import os
from datetime import datetime, timedelta
import threading
import time
import face_recognition
import argparse

"""Функции register_faces_by_web() и register_face_from_image() просто будут вызываться вручную на стрице админа
    По поводу вызова с параметрами, я сделал параметры, чтобы было удобнее показывать Рафу. Так они не нужны, все
    функции можно просто вызывать и все. 
    По поводу функций распознавания - по сути это одна и та же функция webcam_face_recognition(). Она ничего не возвращает,
    иначе будет еще более костально - начать, опознать, завершить и все это заново. Сейчас она работает просто бесконечно,
    пока ее не выключить. Я думаю так и надо. На выход и на выход одна и та же функция, просто скопировать ее. В коде отметил,
    где костыль, чтобы он бесконечно на одной станции человека не распознавал, туда я бы просто вставил не список, а обарщение  
    к БД и все, чтобы сильно не париться, соовтетсвенной копии №1 функции webcam_face_recognition() вствляется вермя и 
    флаг, что трудяга зашел, а в копии №2 распознавание и что он вышел, далее там уже время считается. Запускать их в два потока
    (хз скок у нас потоков будет)
    В функциях все просто захватываются, выключаются камеры - cv2.VideoCapture(0) - захватить изображение, ret, frame = cap.read()
    - считывать, cv2.imshow() - показывать, cv2.destroyAllWindows()- выключить
"""


def register_faces_by_web():
    name = input()

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

                filename = f'./registered_faces/{name}_{photo_count}.jpg'
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

    while (datetime.now() - start_time) < timedelta(seconds=10):
        ret, frame = cap.read()

        if not ret or frame.shape[0] == 0 or frame.shape[1] == 0:
            continue

        cv2.imshow('Webcam', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    processing_thread.join()


def register_face_from_image(image_path, output_directory, output_filename):
    img = face_recognition.load_image_file(image_path)

    face_locations = face_recognition.face_locations(img)
    if len(face_locations) == 0:
        print("No faces found in the provided image.")
        return

    top, right, bottom, left = face_locations[0]
    face_image = img[top:bottom, left:right]

    output_path = os.path.join(output_directory, output_filename)
    cv2.imwrite(output_path, cv2.cvtColor(face_image, cv2.COLOR_RGB2BGR))
    print(f"Face registered! Image saved as {output_path}")


def webcam_face_recognition():
    known_faces = []
    known_face_names = []
    entered_workers = []  # костыльный список для вошедших пользователей

    for filename in os.listdir('registered_faces'):
        image_path = os.path.join('registered_faces', filename)
        img = face_recognition.load_image_file(image_path)
        encoding = face_recognition.face_encodings(img)[0]
        known_faces.append(encoding)
        known_face_names.append(os.path.splitext(filename)[0])

    cap = cv2.VideoCapture(0)

    cap.set(3, 640)  # Ширина
    cap.set(4, 480)  # Высота

    while True:
        ret, frame = cap.read()

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
                if worker not in entered_workers:
                    entered_workers.append(worker)
                    print(f"Match found: {worker}")
                cv2.putText(frame, worker, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2,
                            cv2.LINE_AA)

        cv2.imshow('Webcam', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# То же самое что и в функции выше, только без цикла
def webcam_face_recognition_byFrame():
    known_faces = []
    known_face_names = []
    entered_workers = []  # костыльный список для вошедших пользователей

    for filename in os.listdir('registered_faces'):
        image_path = os.path.join('registered_faces', filename)
        img = face_recognition.load_image_file(image_path)
        encoding = face_recognition.face_encodings(img)[0]
        known_faces.append(encoding)
        known_face_names.append(os.path.splitext(filename)[0])

    cap = cv2.VideoCapture(0)

    cap.set(3, 640)  # Ширина
    cap.set(4, 480)  # Высота


    ret, frame = cap.read()

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
            if worker not in entered_workers:
                entered_workers.append(worker)
                print(f"Match found: {worker}")

            cv2.putText(frame, worker, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2,
                        cv2.LINE_AA)
            return worker

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--action", type=str, required=True)
    parser.add_argument(
        "--file", type=str, required=False)
    parser.add_argument(
        "--name", type=str, required=False)
    args = parser.parse_args()
    action = args.action
    file = args.file
    name = args.name
    if action is None:
        print("Argument error!")
    elif action == "entry":
        res = webcam_face_recognition_byFrame()
        print(res)
    elif action == "registration" and file is None:
        register_faces_by_web()
    elif action == "registration" and file is not None:
        image_path = f"/Users/yura/PycharmProjects/raf_course_work/faceID/files/{file}"
        output_directory = "registered_faces"
        output_filename = f"{file}"

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        register_face_from_image(image_path, output_directory, output_filename)
