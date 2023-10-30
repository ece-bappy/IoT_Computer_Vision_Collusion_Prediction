import cv2
import imutils
import numpy as np
import argparse

# Step 2: Create a model for human detection
HOGCV = cv2.HOGDescriptor()
HOGCV.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


# Step 3: Define the detect() method
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
    return frame


# Step 4: Create the humanDetector() method
def humanDetector(args):
    image_path = args["image"]
    video_path = args["video"]
    if str(args["camera"]) == "true":
        camera = True
    else:
        camera = False
    writer = None
    if args["output"] is not None and image_path is None:
        writer = cv2.VideoWriter(
            args["output"], cv2.VideoWriter_fourcc(*"MJPG"), 10, (600, 600)
        )
    if camera:
        print("[INFO] Opening Web Cam.")
        detectByCamera(writer)
    elif video_path is not None:
        print("[INFO] Opening Video from path.")
        detectByPathVideo(video_path, writer)
    elif image_path is not None:
        print("[INFO] Opening Image from path.")
        detectByPathImage(image_path, args["output"])


# Step 5: Implement the detectByCamera() method
def detectByCamera(writer):
    video = cv2.VideoCapture(0)
    print("Detecting people...")
    while True:
        check, frame = video.read()
        frame = detect(frame)
        if writer is not None:
            writer.write(frame)
        key = cv2.waitKey(1)
        if key == ord("q"):
            break
    video.release()
    cv2.destroyAllWindows()


# Step 6: Implement the detectByPathVideo() method
def detectByPathVideo(path, writer):
    video = cv2.VideoCapture(path)
    check, frame = video.read()
    if not check:
        print(
            "Video Not Found. Please Enter a Valid Path (Full path of Video Should be Provided)."
        )
        return
    print("Detecting people...")
    while video.isOpened():
        check, frame = video.read()
        if check:
            frame = imutils.resize(frame, width=min(800, frame.shape[1]))
            frame = detect(frame)
            if writer is not None:
                writer.write(frame)
            key = cv2.waitKey(1)
            if key == ord("q"):
                break
        else:
            break
    video.release()
    cv2.destroyAllWindows()


# Step 7: Implement the detectByPathImage() method
def detectByPathImage(path, output_path):
    image = cv2.imread(path)
    image = imutils.resize(image, width=min(800, image.shape[1]))
    result_image = detect(image)
    if output_path is not None:
        cv2.imwrite(output_path, result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Step 8: Define the argsParser() method
def argsParser():
    arg_parse = argparse.ArgumentParser()
    arg_parse.add_argument("-v", "--video", default=None, help="Path to Video File")
    arg_parse.add_argument("-i", "--image", default=None, help="Path to Image File")
    arg_parse.add_argument(
        "-c", "--camera", default=False, help="Set true if you want to use the camera."
    )
    arg_parse.add_argument(
        "-o", "--output", type=str, help="Path to optional output video file"
    )
    args = vars(arg_parse.parse_args())
    return args


# Step 9: Create the main function
if __name__ == "__main__":
    HOGCV = cv2.HOGDescriptor()
    HOGCV.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    args = argsParser()
    humanDetector(args)
