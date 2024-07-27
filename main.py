import cv2
import pyautogui
import time
import mss
import mss.tools
import cv2
import numpy as np


confirm_button_template = cv2.imread('./images/confirmbet.png')
cancel_button_template = cv2.imread('./images/cancelbet.png')
crash_template = cv2.imread('./images/crash.png')
multipler_template = cv2.imread('./images/multipler.png')
win_template = cv2.imread('./images/gamewin.png')
bet_template = cv2.imread('./images/bet.png')
setupbet_template = cv2.imread('./images/setupbet.png')
finishsetup_template = cv2.imread('./images/notfinish.png')

def click_button(button_positions, num_positions):
    num_positions = min(num_positions, len(button_positions))

    for i in range(num_positions):
        x, y, w, h = button_positions[i]
        center_x = x + w // 2
        center_y = y + h // 2

        pyautogui.moveTo(center_x, center_y, duration=0.2)
        pyautogui.click()
        time.sleep(0.3)

def detect_button(image, button_template, threshold):
    w, h = button_template.shape[1], button_template.shape[0]

    res = cv2.matchTemplate(image, button_template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)

    button_positions = []
    for pt in zip(*loc[::-1]):
        button_positions.append((pt[0], pt[1], w, h))
        cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)

    return button_positions

def capture_screen():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)
        img = np.array(screenshot)

        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img

def run(input_round):
    round = 0
    running = True
    print("Starting the script...")
    while running:
        if round == input_round:
            print("Finished all rounds.")
            running = False
            break
        
        screen_image = capture_screen()
        finishsetup_positions = detect_button(screen_image, finishsetup_template, 0.9)
        if finishsetup_positions:
            print("Finish setup not found. Setting up auto bet...")
            setup()
        
        screen_image = capture_screen()
        crash_positions = detect_button(screen_image, crash_template, 0.7)
        if crash_positions:
            crash(running)

        confirm_positions = detect_button(screen_image, confirm_button_template, 0.7)
        if confirm_positions:
            click_button(confirm_positions, 1)
            round += 1
            print("Clicked Confirm button.")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

def crash(running):
    print("Crash detected. Waiting for multiplier.")
    multipler_positions = None

    while not multipler_positions and running:
        screen_image = capture_screen()
        multipler_positions = detect_button(screen_image, multipler_template, 0.7)
        if multipler_positions:
            print("Multiplier detected.")
            click_button(multipler_positions, 2)
            print("Clicked Multiplier button.")
            time.sleep(0.5)

    confirm_positions = None
    while not confirm_positions and running:
        screen_image = capture_screen()
        confirm_positions = detect_button(screen_image, confirm_button_template, 0.7)
        if confirm_positions:
            click_button(confirm_positions, 1)
            print("Clicked Confirm button.")
            time.sleep(0.5)

    win_positions = None
    while not win_positions and running:
        screen_image = capture_screen()
        win_positions = detect_button(screen_image, win_template, 0.7)
        crash_positions = detect_button(screen_image, crash_template, 0.7)

        if win_positions:
            print("Win detected.")
            bet_position = None
            print("Waiting for bet button...")
            while not bet_position and running:
                screen_image = capture_screen()
                bet_position = detect_button(screen_image, bet_template, 0.7)
                if bet_position:
                    print("Resetting bet...")
                    click_button(bet_position, 1)
                    time.sleep(0.5)
                    pyautogui.typewrite("2000")
                    pyautogui.press('enter')
                    time.sleep(0.5)
                    print("Bet reset.")

        elif crash_positions:
            crash(running)
            return

def setup():
    while True:
        screen_image = capture_screen()
        setupbet_positions = detect_button(screen_image, setupbet_template, 0.9)
        if setupbet_positions:
            print("Setup bet detected... Setting up auto bet...")
            x, y, w, h = setupbet_positions[0]
            betclick_x = x + (w * 0.75)
            betclick_y = y + (h * 0.25)

            betbutton_x = x + (w * 0.10)
            betbutton_y = y + (h * 0.25)

            pyautogui.moveTo(betclick_x, betclick_y, duration=0.5)
            time.sleep(0.5)
            pyautogui.click()
            time.sleep(0.5)
            pyautogui.typewrite("1.3")
            time.sleep(0.5)
            pyautogui.press('enter')
            time.sleep(0.5)
            
            pyautogui.moveTo(betbutton_x, betbutton_y, duration=0.5)
            time.sleep(0.5)
            pyautogui.click()
            time.sleep(0.5)
            print("Auto bet setup complete.")
            break

if __name__ == '__main__':
    input_round = int(input("Enter number of rounds: "))
    run(input_round)