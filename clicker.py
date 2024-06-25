import pyautogui
import time

def click_button(button_positions, num_positions):
    # Ensure num_positions does not exceed the length of button_positions
    num_positions = min(num_positions, len(button_positions))

    for i in range(num_positions):
        x, y, w, h = button_positions[i]
        # Calculate the center of the detected button
        center_x = x + w // 2
        center_y = y + h // 2

        # Move the cursor to the center of the button and click
        pyautogui.moveTo(center_x, center_y, duration=0.2)  # Adding a small delay
        pyautogui.click()
        time.sleep(0.3)