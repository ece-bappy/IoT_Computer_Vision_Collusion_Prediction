# warning ok, all logic ok, image can be sent

import numpy as np
import cv2
import time
from pushbullet import Pushbullet
import datetime


# Function to add a green overlay and a Warning text to the frame
def flash_frame(frame, text="WARNING!!"):
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (frame.shape[1], frame.shape[0]), (0, 255, 0), -1)

    # Get the size of the text
    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 2, 3)[0]

    # Get the (x, y) coordinates where the text should be displayed
    text_x = (frame.shape[1] - text_size[0]) // 2
    text_y = (frame.shape[0] + text_size[1]) // 2

    # Add text to the overlay
    cv2.putText(
        overlay, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3
    )

    alpha = 0.6  # Transparency factor
    return cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)


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

# The output will be written to output.avi
# out = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc(*"MJPG"), 15.0, (640, 480))

last_notification_time = 0  # Variable to keep track of the last notification time
people_detection_start_time = (
    0  # Variable to keep track of when 4 or more people are first detected
)

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

    remaining_time = 20 - (current_time - last_notification_time)
    remaining_time = max(0, remaining_time)  # Ensure remaining time is not negative
    countdown_label = f"Next notification in: {int(remaining_time)}s"
    cv2.putText(
        frame, countdown_label, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2
    )

    if num_people >= 7:
        if people_detection_start_time == 0:
            people_detection_start_time = current_time

        if current_time - people_detection_start_time >= 1 and remaining_time <= 0:
            # Flash the frame three times before sending notification
            for _ in range(2):
                # Original frame with Warning text
                cv2.imshow("frame", frame)
                cv2.waitKey(100)

                # Flash overlay with Warning text
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

    # out.write(frame.astype("uint8"))
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
# out.release()
cv2.destroyAllWindows()
cv2.waitKey(1)
