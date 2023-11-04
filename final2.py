import numpy as np
import cv2
import time
from pushbullet import Pushbullet
import datetime
import asyncio

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


# Function to capture snapshot and send Pushbullet notification
async def send_notification(snapshot_filename, num_people):
    with open(snapshot_filename, "rb") as pic:
        file_data = pb.upload_file(pic, snapshot_filename)
        push = pb.push_file(
            **file_data,
            body=f"{num_people} People seen near Wazed Building",
            title="Conflict Alert!!",
        )


async def video_processing():
    global start_recording
    last_notification_time = 0

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

        remaining_time = 10 - (current_time - last_notification_time)
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

        if num_people >= 4:
            if current_time - last_notification_time >= 4:
                if not start_recording:
                    # Record the time when the notification is sent
                    notification_time = time.time()

                    snapshot_filename = "snapshot.jpg"
                    save_frame(frame, snapshot_filename)

                    await send_notification(snapshot_filename, num_people)

                    last_notification_time = current_time
                    start_recording = True  # Set the flag to start recording

        cv2.imshow("frame", frame)

        if start_recording and time.time() - notification_time >= 4:
            # Start recording a 5-second clip 4 seconds after the notification is sent
            recording_start_time = time.time()
            recording_end_time = recording_start_time + 5

            # Create a VideoWriter for the clip
            clip_out = cv2.VideoWriter(
                "clip.avi", cv2.VideoWriter_fourcc(*"MJPG"), 15.0, (640, 480)
            )

            while time.time() < recording_end_time:
                ret, frame = cap.read()
                frame = cv2.resize(frame, (640, 480))
                clip_out.write(frame.astype("uint8"))

            clip_out.release()
            start_recording = False  # Reset the flag

            with open("clip.avi", "rb") as video_file:
                video_data = pb.upload_file(video_file, "clip.avi")
            push = pb.push_file(
                **video_data,
                body="5-second video clip after 4 people detected",
                title="Video Alert!!",
            )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


# Run the video processing asynchronously
asyncio.run(video_processing())
