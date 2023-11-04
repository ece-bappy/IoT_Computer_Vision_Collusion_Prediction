import numpy as np
import cv2
import time
from pushbullet import Pushbullet
import datetime

# Import the necessary functions from the first script
from video_capture_and_notification import (
    send_notification_with_snapshot,
    record_and_send_video_notification,
)

# Initialize a variable to keep track of the time the notification was sent
notification_time = 0

# Initialize a flag to indicate whether to start recording
start_recording = False


# Function to add a green overlay and a Warning text to the frame
def flash_frame(frame, text="Warning"):
    return frame  # Return the original frame without any overlay


def save_frame(frame, filename="snapshot.jpg"):
    cv2.imwrite(filename, frame)


# Initialize Pushbullet with your API key
pushbullet_api_key = "o.liL3iwJgHsdp03ESiRf7Q3cPDu06874D"
pb = Pushbullet(pushbullet_api_key)

# Initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cv2.startWindowThread()

# Open webcam video stream
cap = cv2.VideoCapture(0)

last_notification_time = 0  # Variable to keep track of the last notification time
people_detection_start_time = (
    0  # Variable to keep track of when 4 or more people are first detected
)

while True:
    ret, frame = cap.read()

    # Check if the frame is not empty (valid)
    if not ret or frame is None:
        continue  # Skip the rest of the loop and try again

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
    current_date_time = now.strftime(
        "%Y-%m-%d %H:%M:%S"
    )  # Format the date and time as a string

    # Display current date and time on the frame
    cv2.putText(
        frame,
        current_date_time,
        (10, 470),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 255, 0),
        1,
    )

    remaining_time = 30 - (current_time - last_notification_time)
    remaining_time = max(0, remaining_time)  # Ensure remaining time is not negative
    countdown_label = f"Next notification in: {int(remaining_time)}s"
    cv2.putText(
        frame, countdown_label, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2
    )

    if num_people >= 4:
        if people_detection_start_time == 0:
            people_detection_start_time = current_time

        if current_time - people_detection_start_time >= 1 and remaining_time <= 0:
            # Record the time when the notification is sent
            notification_time = time.time()

            # Send a notification with a snapshot
            send_notification_with_snapshot(pb, num_people, frame)

            last_notification_time = current_time
            people_detection_start_time = 0
            start_recording = True  # Set the flag to start recording

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

    if start_recording and time.time() - notification_time >= 4:
        # Start recording a 5-second clip 4 seconds after the notification is sent
        record_and_send_video_notification(pb)
        start_recording = False  # Reset the flag

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
cv2.waitKey(1)
