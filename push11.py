import numpy as np
import cv2
import time
from pushbullet import Pushbullet

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
out = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc(*"MJPG"), 15.0, (640, 480))

last_notification_time = 0  # Variable to keep track of the last notification time

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Resizing for faster detection
    frame = cv2.resize(frame, (640, 480))

    # Detect people in the image
    boxes, weights = hog.detectMultiScale(frame, winStride=(8, 8))

    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

    # Count the number of detected people
    num_people = len(boxes)

    current_time = time.time()  # Get the current time

    remaining_time = 60 - (
        current_time - last_notification_time
    )  # Calculate remaining time

    # Display the countdown on the screen
    countdown_label = f"Next notification in: {max(0, int(remaining_time))}s"
    cv2.putText(
        frame,
        countdown_label,
        (10, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 0, 255),
        2,
    )

    if num_people >= 4 and remaining_time <= 0:
        # Send a notification to your smartphone
        push_title = "People Detected"
        push_message = f"Number of people detected: {num_people}"
        push = pb.push_note(push_title, push_message)

        last_notification_time = current_time  # Update the last notification time

    for i, (xA, yA, xB, yB) in enumerate(boxes):
        # Display the detected boxes in the color picture
        cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)

        # Display the label above the detected person
        person_label = f"Person{i + 1}"
        cv2.putText(
            frame,
            person_label,
            (xA, yA - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2,
        )

    # Write the output video
    out.write(frame.astype("uint8"))
    # Display the resulting frame
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# When everything done, release the capture
cap.release()
# Release the output
out.release()
# Finally, close the window
cv2.destroyAllWindows()
cv2.waitKey(1)
