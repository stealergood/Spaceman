import mss
import mss.tools
import cv2
import numpy as np

def capture_screen():
    with mss.mss() as sct:
        # Capture the entire screen (default to the first monitor)
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)
        img = np.array(screenshot)

        # Convert the image from BGRA to BGR
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img
    
