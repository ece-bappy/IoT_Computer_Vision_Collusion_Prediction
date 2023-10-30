import cv2
import mediapipe as mp

# Initialize MediaPipe Pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Initialize VideoCapture to capture video from your camera
cap = cv2.VideoCapture(0)  # Use 0 for the default camera

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Convert the frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with the Pose model
    results = pose.process(frame_rgb)

    if results.pose_landmarks:
        # Get the bounding box coordinates for the detected body
        landmarks = results.pose_landmarks.landmark
        height, width, _ = frame.shape
        min_x, min_y, max_x, max_y = width, height, 0, 0

        for lm in landmarks:
            x, y = int(lm.x * width), int(lm.y * height)
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)

        # Draw the bounding box around the body
        cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (0, 255, 0), 2)

    # Display the frame with bounding box
    cv2.imshow("Body Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
