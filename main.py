import sys
import cv2
import keyboard
import pyautogui
import time
import captureScreen
import imageDetection
import clicker
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, 
                             QVBoxLayout, QHBoxLayout, QMessageBox, QRadioButton, QButtonGroup)
from PyQt5.QtGui import QPixmap

class CrashBotGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.mode = 0
        self.input_round = 0
        self.running = False
        
        self.confirm_button_template = cv2.imread('./images/confirmbet.png')
        self.cancel_button_template = cv2.imread('./images/cancelbet.png')
        self.crash_template = cv2.imread('./images/crash.png')
        self.multipler_template = cv2.imread('./images/multipler.png')
        self.win_template = cv2.imread('./images/gamewin.png')
        self.bet_template = cv2.imread('./images/bet.png')

    def initUI(self):
        self.setWindowTitle('Spaceman Bot')
        
        image_label = QLabel(self)
        pixmap = QPixmap('./images/spacemanlogo.png')
        image_label.setPixmap(pixmap)
        
        mode_label = QLabel('Select Mode:', self)
        keterangan_label = QLabel('Mode 1: Stop bet di x1.3 (modal aman minimal 500rb)\nMode 2: Stop bet di x2 (modal aman minimal 1jt)', self)
        
        self.mode1_radio = QRadioButton("Mode 1", self)
        self.mode2_radio = QRadioButton("Mode 2", self)
        self.mode1_radio.setChecked(True)

        self.mode_group = QButtonGroup(self)
        self.mode_group.addButton(self.mode1_radio)
        self.mode_group.addButton(self.mode2_radio)
        
        round_label = QLabel('Masukkan Jumlah Round:', self)
        self.round_input = QLineEdit(self)
        
        start_button = QPushButton('Start', self)
        start_button.clicked.connect(self.start_bot)
        
        stop_button = QPushButton('Stop', self)
        stop_button.clicked.connect(self.stop_bot)
        
        self.setFixedSize(430, 500)
        
        layout = QVBoxLayout()
        layout.addWidget(image_label)
        layout.addWidget(mode_label)
        layout.addWidget(keterangan_label)
        layout.addWidget(self.mode1_radio)
        layout.addWidget(self.mode2_radio)
        layout.addWidget(round_label)
        layout.addWidget(self.round_input)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(start_button)
        button_layout.addWidget(stop_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)

    def start_bot(self):
        self.input_round = int(self.round_input.text())
        self.mode = 0
        if self.mode1_radio.isChecked():
            self.mode = 2
        elif self.mode2_radio.isChecked():
            self.mode = 1
        else:
            QMessageBox.critical(self, 'Error', 'Invalid mode. Exiting...')
            return
        
        self.running = True
        self.run_bot()

    def stop_bot(self):
        self.running = False
        QMessageBox.information(self, 'Info', 'Bot stopped.')

    def run_bot(self):
        round = 0
        print("Starting the script...")
        while self.running:
            if round == self.input_round:
                print("Finished all rounds.")
                break

            screen_image = captureScreen.capture_screen()

            crash_positions = imageDetection.detect_button(screen_image, self.crash_template)
            if crash_positions:
                self.crash(self.mode)

            confirm_positions = imageDetection.detect_button(screen_image, self.confirm_button_template)
            if confirm_positions:
                clicker.click_button(confirm_positions, 1)
                round += 1
                print("Clicked Confirm button.")

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if keyboard.is_pressed('q'):
                break

        cv2.destroyAllWindows()

    def crash(self, mode):
        print("Crash detected. Waiting for multiplier.")
        multipler_positions = None

        while not multipler_positions and self.running:
            screen_image = captureScreen.capture_screen()
            multipler_positions = imageDetection.detect_button(screen_image, self.multipler_template)
            if multipler_positions:
                print("Multiplier detected.")
                clicker.click_button(multipler_positions, mode)
                print("Clicked Multiplier button.")
                time.sleep(0.5)

        confirm_positions = None
        while not confirm_positions and self.running:
            screen_image = captureScreen.capture_screen()
            confirm_positions = imageDetection.detect_button(screen_image, self.confirm_button_template)
            if confirm_positions:
                clicker.click_button(confirm_positions, 1)
                print("Clicked Confirm button.")
                time.sleep(0.5)

        win_positions = None
        while not win_positions and self.running:
            screen_image = captureScreen.capture_screen()
            win_positions = imageDetection.detect_button(screen_image, self.win_template)
            crash_positions = imageDetection.detect_button(screen_image, self.crash_template)

            if win_positions:
                print("Win detected.")
                bet_position = None
                print("Waiting for bet button...")
                while not bet_position and self.running:
                    screen_image = captureScreen.capture_screen()
                    bet_position = imageDetection.detect_button(screen_image, self.bet_template)
                    if bet_position:
                        print("Resetting bet...")
                        clicker.click_button(bet_position, 1)
                        time.sleep(0.5)
                        pyautogui.typewrite("2000")
                        pyautogui.press('enter')
                        time.sleep(0.5)
                        print("Bet reset.")

            elif crash_positions:
                self.crash(mode)
                return

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CrashBotGUI()
    ex.show()
    sys.exit(app.exec_())
