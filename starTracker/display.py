import Adafruit_CharLCD as LCD
from planets import planets
import time


class Display:

    def __init__(self):
        # init the LCD
        self.lcd = LCD.Adafruit_CharLCDPlate()

        # set color to red
        self.lcd.set_color(1, 0, 0)
        self.lcd.message('Initializing...\n')
        self.modes = {"Main": self.main_menu, "Observation": self.observation_mode, "Photography": self.photo_mode}
        self.options = None
        self.buttons = [[LCD.SELECT, 0], [LCD.LEFT, 0], [LCD.RIGHT,0],
                        [LCD.DOWN, 1], [LCD.UP, -1]]

    def main_menu(self):
        self.lcd.clear()
        self.options = ['Observation', "Photography"]
        index = 0
        self.lcd.message(self.options[index])
        while True:
            for button in self.buttons:
                if self.lcd.is_pressed(button[0]):
                    self.lcd.clear()
                    if button[1] == 0: # You've Pressed Select
                        self.modes[button[index]]()
                    elif index == len(self.options) - 1 and button[1] == 1:
                        index = 0
                    elif index == 0 and button[1] == -1:
                        index = len(self.options) - 1
                    else:
                        index += button[1]
                    self.lcd.message("{0} - {1}".format(self.options[index], index))
                    time.sleep(0.25)


    def observation_mode(self):
        self.lcd.clear()
        self.options = list(planets.keys())
        index = 0
        self.options.append("Back")
        self.lcd.message(self.options[index])
        while True:
            for button in self.buttons:
                if self.lcd.is_pressed(button[0]):
                    self.lcd.clear()
                    if index == len(self.options) - 1 and button[1] == 1:
                        index = 0
                    elif index == 0 and button[1] == -1:
                        index = len(self.options) - 1
                    else:
                        index += button[1]
                    self.lcd.message("{0} - {1}".format(self.options[index], index))
                    time.sleep(0.25)


    def photo_mode(self):
        self.lcd.message("Entered Photo Mode!")


if __name__ == '__main__':
    disp = Display()
    disp.main_menu()
