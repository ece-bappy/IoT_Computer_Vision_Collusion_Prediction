import numpy as np
import cv2
import time
from pushbullet import Pushbullet
import datetime
import serial

# Arduino Serial Port (change to the appropriate port)
arduino_port = "COM5"
arduino = serial.Serial(arduino_port, baudrate=9600, timeout=1)


# Function to read the potentiometer value from Arduino
def read_potentiometer_value():
    arduino.write(b"r")  # Send a request to Arduino to send the potentiometer value
    arduino_value = arduino.readline().decode().strip()
    return int(arduino_value)


# Rest of your code remains the same

# Initialize Pushbullet with your API key
pushbullet_api_key = "o.liL3iwJgHsdp03ESiRf7Q3cPDu06874D"
pb = Pushbullet(pushbullet_api_key)

# ... (rest of your code)

while True:
    # Rest of your code remains the same

    # Read potentiometer value from Arduino
    potentiometer_value = read_potentiometer_value()

    # Check if there are more than 6 people and potentiometer value is between 900 and 1000
    if num_people >= 7 and 900 <= potentiometer_value <= 1000:
        if people_detection_start_time == 0:
            people_detection_start_time = current_time

        if current_time - people_detection_start_time >= 2 and remaining_time <= 0:
            # Flash the frame three times before sending notification
            for _ in range(3):
                # Original frame with Warning text
                cv2.imshow("frame", frame)
                cv2.waitKey(100)

                # Flash overlay with Warning text
                flashed_frame = flash_frame(frame)
                cv2.imshow("frame", flashed_frame)
                cv2.waitKey(100)

            # Capture a 5-second video clip
            fourcc = cv2.VideoWriter_fourcc(*"XVID")
            video_filename = "clip.avi"
            out = cv2.VideoWriter(video_filename, fourcc, 20.0, (640, 480))
            start_time = time.time()

            while time.time() - start_time < 5:
                ret, video_frame = cap.read()
                out.write(video_frame)

            out.release()

            snapshot_filename = "snapshot.jpg"
            save_frame(frame, snapshot_filename)

            # Send video clip, snapshot, and notification
            with open(video_filename, "rb") as video:
                video_data = pb.upload_file(video, video_filename)

            with open(snapshot_filename, "rb") as pic:
                pic_data = pb.upload_file(pic, snapshot_filename)

            push = pb.push_file(
                **video_data,
                body=f"{num_people} People seen near Wazed Building",
                title="Conflict Alert!! - Video Clip",
            )

            push = pb.push_file(
                **pic_data,
                body="Snapshot",
                title="Conflict Alert!! - Snapshot",
            )

            last_notification_time = current_time
            people_detection_start_time = 0
    else:
        people_detection_start_time = 0

    # ... (rest of your code)

# Close the Arduino serial connection when done
arduino.close()
