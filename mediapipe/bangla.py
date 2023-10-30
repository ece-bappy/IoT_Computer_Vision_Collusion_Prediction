import cv2
import numpy as np

# Load your Bengali font from the same directory as your Python script
font_path = "bng.ttf"

# Font properties
font_scale = 1
font_color = (255, 255, 255)
font_thickness = 2

# Text to display in Bengali (Unicode encoding)
bengali_text = "বাংলা টেক্সট"

print("বাংলা টেক্সট")

# Create a black image
image = np.zeros((400, 600, 3), dtype=np.uint8)

# Load the Bengali font
bengali_font = cv2.FONT_HERSHEY_COMPLEX
try:
    cv2.putText(
        image,
        bengali_text,
        (50, 200),
        bengali_font,
        font_scale,
        font_color,
        font_thickness,
    )
except:
    print(
        "Font loading error. Make sure 'bornomala.ttf' is in the same directory as your Python script."
    )

# Display the image
cv2.imshow("Bengali Text", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
