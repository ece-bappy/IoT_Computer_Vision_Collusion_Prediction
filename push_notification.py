from pushbullet import Pushbullet
import cv2
import time

# Initialize Pushbullet with your API key
pushbullet_api_key = "o.liL3iwJgHsdp03ESiRf7Q3cPDu06874D"
pb = Pushbullet(pushbullet_api_key)


def send_notification_snapshot(num_people, frame):
    snapshot_filename = "snapshot.jpg"
    save_frame(frame, snapshot_filename)
    with open(snapshot_filename, "rb") as pic:
        file_data = pb.upload_file(pic, snapshot_filename)
        push = pb.push_file(
            **file_data,
            body=f"{num_people} People seen near Wazed Building",
            title="Conflict Alert!!",
        )


def send_notification_video(num_people):
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

    with open("clip.avi", "rb") as video_file:
        video_data = pb.upload_file(video_file, "clip.avi")
    push = pb.push_file(
        **video_data,
        body="5-second video clip after 4 people detected",
        title="Video Alert!!",
    )


def save_frame(frame, filename="snapshot.jpg"):
    cv2.imwrite(filename, frame)


# Check if this script is being run as the main script
if __name__ == "__main__":
    # You can add code here to handle notifications as needed
    pass
