import cv2
import time
from pushbullet import Pushbullet


def save_frame(frame, filename="snapshot.jpg"):
    cv2.imwrite(filename, frame)


def send_notification_with_snapshot(pb, num_people, frame):
    snapshot_filename = "snapshot.jpg"
    save_frame(frame, snapshot_filename)
    with open(snapshot_filename, "rb") as pic:
        file_data = pb.upload_file(pic, snapshot_filename)
        push = pb.push_file(
            **file_data,
            body=f"{num_people} People seen near Wazed Building",
            title="Conflict Alert!!",
        )


def record_and_send_video_notification(pb):
    recording_start_time = time.time()
    recording_end_time = recording_start_time + 3  # 5-second video clip

    cap = cv2.VideoCapture(0)
    out = cv2.VideoWriter("clip.avi", cv2.VideoWriter_fourcc(*"MJPG"), 15.0, (640, 480))

    while time.time() < recording_end_time:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (640, 480))
        out.write(frame.astype("uint8"))

    out.release()
    cap.release()

    with open("clip.avi", "rb") as video_file:
        video_data = pb.upload_file(video_file, "clip.avi")
    push = pb.push_file(
        **video_data,
        body="5-second video clip after 4 people detected",
        title="Video Alert!!",
    )


if __name__ == "__main__":
    # Initialize Pushbullet with your API key
    pushbullet_api_key = "o.liL3iwJgHsdp03ESiRf7Q3cPDu06874D"
    pb = Pushbullet(pushbullet_api_key)

    while True:
        # Monitor a queue or trigger from the main script to initiate tasks
        # For example, use a message or flag from the main script to start recording and sending notifications
        # You may use an event or message-passing mechanism as needed
        pass  # Add the necessary code or logic here
