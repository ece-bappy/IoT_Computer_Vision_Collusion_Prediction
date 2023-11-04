import numpy as np
import cv2
import time
import datetime
import subprocess  # Import subprocess module for running the push_notification.py script

# Initialize a variable to keep track of the time the notification was sent
notification_time = 0

# Initialize a flag to indicate whether to start recording
start_recording = False

# Initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cv2.startWindowThread()

# Open webcam video stream
cap = cv2.VideoCapture(0)

# The output will be written to output.avi
out = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc(*"MJPG"), 15.0, (640, 480))

last_notification_time = 0  # Variable to keep track of the last notification time
people_detection_start_time = (
    0  # Variable to keep track of when 4 or more people are first detected
)


def send_notification():
    subprocess.run(
        ["python", "push_notification.py"], check=True
    )  # Run the push_notification.py script


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

    remaining_time = 10 - (current_time - last_notification_time)
    remaining_time = max(0, remaining_time)  # Ensure remaining time is not negative

    if num_people >= 4:
        if people_detection_start_time == 0:
            people_detection_start_time = current_time

        if current_time - people_detection_start_time >= 1 and remaining_time <= 0:
            # Record the time when the notification is sent
            notification_time = time.time()

            last_notification_time = current_time
            people_detection_start_time = 0
            start_recording = True  # Set the flag to start recording

            if num_people >= 4:
                send_notification()  # Call the send_notification function

    else:
        people_detection_start_time = 0

    out.write(frame.astype("uint8"))
    cv2.imshow("frame", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
cv2.waitKey(1)
