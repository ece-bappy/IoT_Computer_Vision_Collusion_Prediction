import pyaudio
import numpy as np
import cv2
import time
import keyboard
from pushbullet import Pushbullet
import datetime


# Function to add a green overlay and a Warning text to the frame
def flash_frame(frame, text="WARNING!!"):
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (frame.shape[1], frame.shape[0]), (0, 255, 0), -1)

    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 2, 3)[0]
    text_x = (frame.shape[1] - text_size[0]) // 2
    text_y = (frame.shape[0] + text_size[1]) // 2

    cv2.putText(
        overlay, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3
    )

    alpha = 0.6  # Transparency factor
    return cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)


def save_frame(frame, filename="snapshot.jpg"):
    cv2.imwrite(filename, frame)


pushbullet_api_key = "o.liL3iwJgHsdp03ESiRf7Q3cPDu06874D"
pb = Pushbullet(pushbullet_api_key)

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cv2.startWindowThread()

cap = cv2.VideoCapture(1)

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

audio = pyaudio.PyAudio()

stream = audio.open(
    format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
)

print("Real-time noise level monitoring...")

audio_data = []

last_notification_time = 0
people_detection_start_time = 0

try:
    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (640, 480))
        boxes, weights = hog.detectMultiScale(frame, winStride=(8, 8))
        boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
        num_people = len(boxes)
        current_time = time.time()
        now = datetime.datetime.now()
        num_people_label = f"Number of people: {num_people}"
        cv2.putText(
            frame,
            num_people_label,
            (10, 450),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 0, 12),
            2,
        )
        current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(
            frame,
            current_date_time,
            (10, 470),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            1,
        )

        remaining_time = 40 - (current_time - last_notification_time)
        remaining_time = max(0, remaining_time)

        countdown_label = f"Next notification in: {int(remaining_time)}s"
        cv2.putText(
            frame,
            countdown_label,
            (10, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2,
        )

        data = stream.read(CHUNK)
        audio_data.extend(np.frombuffer(data, dtype=np.int16))

        if len(audio_data) > RATE:
            audio_data = audio_data[-RATE:]

        rms = np.sqrt(np.mean(np.array(audio_data) ** 2))
        print(f"Current RMS: {rms:.2f} dB")

        if 9 <= rms <= 40 and num_people >= 3:
            if people_detection_start_time == 0:
                people_detection_start_time = current_time

            if current_time - people_detection_start_time >= 3 and remaining_time <= 0:
                for _ in range(2):
                    cv2.imshow("frame", frame)
                    cv2.waitKey(100)

                    flashed_frame = flash_frame(frame)
                    cv2.imshow("frame", flashed_frame)
                    cv2.waitKey(100)

                snapshot_filename = "snapshot.jpg"
                save_frame(frame, snapshot_filename)
                with open(snapshot_filename, "rb") as pic:
                    file_data = pb.upload_file(pic, snapshot_filename)
                    push = pb.push_file(
                        **file_data,
                        body=f"{num_people} People seen near Wazed Building",
                        title="Conflict Alert!!",
                    )

                last_notification_time = current_time
                people_detection_start_time = 0
        else:
            people_detection_start_time = 0

        for i, (xA, yA, xB, yB) in enumerate(boxes):
            cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
            person_label = f"Person{i + 1}"
            cv2.putText(
                frame,
                person_label,
                (xA, yA - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 255),
                2,
            )

        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

except KeyboardInterrupt:
    pass
finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)
