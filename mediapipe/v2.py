import cv2

# Load the pre-trained MobileNet-SSD model
model_weights = "mobilenet_iter_73000.caffemodel"
model_config = "train.prototxt"
net = cv2.dnn.readNetFromCaffe(model_config, model_weights)

# Initialize VideoCapture to capture video from your camera
cap = cv2.VideoCapture(0)  # Use 0 for the default camera

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Prepare the input image for the SSD model
    blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)

    # Set the input to the model
    net.setInput(blob)

    # Perform inference and get the detections
    detections = net.forward()

    # Process the detections
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        # Filter out weak detections
        if confidence > 0.5:  # You can adjust this confidence threshold
            class_id = int(detections[0, 0, i, 1])
            label = "Person"  # Assuming class 15 corresponds to persons in the model

            # Get the coordinates of the bounding box
            box = detections[0, 0, i, 3:7] * np.array(
                [frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]]
            )
            (startX, startY, endX, endY) = box.astype("int")

            # Draw the bounding box and label
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(
                frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2
            )

    # Display the frame with bounding boxes
    cv2.imshow("Person Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
