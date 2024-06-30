import cv2
import keyboard
import pyautogui
import time
import captureScreen
import imageDetection
import clicker

confirm_button_template = cv2.imread('./images/confirmbet.png')
cancel_button_template = cv2.imread('./images/cancelbet.png')
crash_template = cv2.imread('./images/crash.png')
multipler_template = cv2.imread('./images/multipler.png')
win_template = cv2.imread('./images/gamewin.png')
bet_template = cv2.imread('./images/bet.png')
setupbet_template = cv2.imread('./images/setupbet.png')
finishsetup_template = cv2.imread('./images/finishsetup.png')

def run_bot(input_round, mode):
    round = 0
    running = True
    print("Starting the script...")
    while running:
        if round == input_round:
            print("Finished all rounds.")
            break
        
        screen_image = captureScreen.capture_screen()
        finishsetup_positions = imageDetection.detect_button(screen_image, finishsetup_template, 0.9)
        if not finishsetup_positions:
            setup()
            continue
        
        screen_image = captureScreen.capture_screen()
        crash_positions = imageDetection.detect_button(screen_image, crash_template, 0.7)
        if crash_positions:
            crash(mode, running)

        confirm_positions = imageDetection.detect_button(screen_image, confirm_button_template, 0.7)
        if confirm_positions:
            clicker.click_button(confirm_positions, 1)
            round += 1
            print("Clicked Confirm button.")

        if cv2.waitKey(1) & 0xFF == ord('q') or keyboard.is_pressed('q'):
            break

    cv2.destroyAllWindows()

def crash(mode, running):
    print("Crash detected. Waiting for multiplier.")
    multipler_positions = None

    while not multipler_positions and running:
        screen_image = captureScreen.capture_screen()
        multipler_positions = imageDetection.detect_button(screen_image, multipler_template, 0.7)
        if multipler_positions:
            print("Multiplier detected.")
            clicker.click_button(multipler_positions, mode)
            print("Clicked Multiplier button.")
            time.sleep(0.5)

    confirm_positions = None
    while not confirm_positions and running:
        screen_image = captureScreen.capture_screen()
        confirm_positions = imageDetection.detect_button(screen_image, confirm_button_template, 0.7)
        if confirm_positions:
            clicker.click_button(confirm_positions, 1)
            print("Clicked Confirm button.")
            time.sleep(0.5)

    win_positions = None
    while not win_positions and running:
        screen_image = captureScreen.capture_screen()
        win_positions = imageDetection.detect_button(screen_image, win_template, 0.7)
        crash_positions = imageDetection.detect_button(screen_image, crash_template, 0.7)

        if win_positions:
            print("Win detected.")
            bet_position = None
            print("Waiting for bet button...")
            while not bet_position and running:
                screen_image = captureScreen.capture_screen()
                bet_position = imageDetection.detect_button(screen_image, bet_template, 0.7)
                if bet_position:
                    print("Resetting bet...")
                    clicker.click_button(bet_position, 1)
                    time.sleep(0.5)
                    pyautogui.typewrite("2000")
                    pyautogui.press('enter')
                    time.sleep(0.5)
                    print("Bet reset.")

        elif crash_positions:
            crash(mode, running)
            return

def setup():
    while True:
        screen_image = captureScreen.capture_screen()
        setupbet_positions = imageDetection.detect_button(screen_image, setupbet_template, 0.9)
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
    mode = int(input("Enter mode (1 for x2, 2 for x1.3): "))
    run_bot(input_round, mode)
