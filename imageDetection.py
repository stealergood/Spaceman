import cv2
import numpy as np

def detect_button(image, button_template, threshold=0.7):
    # Get the width and height of the button template
    w, h = button_template.shape[1], button_template.shape[0]

    # Perform template matching
    res = cv2.matchTemplate(image, button_template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)

    button_positions = []
    for pt in zip(*loc[::-1]):
        button_positions.append((pt[0], pt[1], w, h))
        # Draw a rectangle around the detected button (optional for debugging)
        cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)

    return button_positions