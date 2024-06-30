import cv2
from imageDetection import detect_button

# Load the images
main_template = cv2.imread("images/main.png", cv2.IMREAD_UNCHANGED)
setupbet_template = cv2.imread("images/notfinish.png", cv2.IMREAD_UNCHANGED)

# Detect the button
positions, image = detect_button(main_template, setupbet_template, 0.9)

# Create a named window
cv2.namedWindow("Detected Image", cv2.WINDOW_NORMAL)

# Resize the window
cv2.resizeWindow("Detected Image", 800, 600)  # Resize to 800x600 pixels

# Show the image in the resized window
cv2.imshow("Detected Image", image)

# Wait for a key press and close the window
cv2.waitKey(0)
cv2.destroyAllWindows()
