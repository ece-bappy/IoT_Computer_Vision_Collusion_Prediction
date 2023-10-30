import cv2

# Initialize the HOG descriptor/person detector
HOGCV = cv2.HOGDescriptor()
HOGCV.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


def detect(frame):
    bounding_box_coordinates, weights = HOGCV.detectMultiScale(
        frame, winStride=(4, 4), padding=(8, 8), scale=1.03
    )

    person = 1
    for x, y, w, h in bounding_box_coordinates:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(
            frame,
            f"Person {person}",
            (x, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 255),
            1,
        )
        person += 1

    cv2.putText(
        frame,
        "Status: Detecting",
        (40, 40),
        cv2.FONT_HERSHEY_DUPLEX,
        0.8,
        (255, 0, 0),
        2,
    )
    cv2.putText(
        frame,
        f"Total Persons: {person-1}",
        (40, 70),
        cv2.FONT_HERSHEY_DUPLEX,
        0.8,
        (255, 0, 0),
        2,
    )
    cv2.imshow("output", frame)


def detectByCamera():
    video = cv2.VideoCapture(0)  # Index set to 0 to use the primary camera
    print("Detecting people...")
    while True:
        check, frame = video.read()
        if not check:  # If frame not received from the camera, break the loop
            break
        detect(frame)
        key = cv2.waitKey(1)
        if key == ord("q"):
            break

    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    detectByCamera()
