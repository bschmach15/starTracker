import Adafruit_CharLCD as LCD
from planets import planets
import time
from threading import Thread


class Display(Thread):

    def __init__(self, queue):
        # init the LCD
        self.lcd = LCD.Adafruit_CharLCDPlate()

        # set color to red
        self.lcd.set_color(1, 0, 0)
        self.lcd.message('Initializing...\n')
        self.modes = {"Main Menu": self.main_menu, "Observation": self.observation_mode, "Photography": self.photo_mode}
        self.options = None
        self.buttons = [[LCD.SELECT, 0], [LCD.LEFT, "Back"], [LCD.RIGHT,3],
                        [LCD.DOWN, 1], [LCD.UP, -1]]
        # self.main_menu()
        self.q = queue
        Thread.__init__(self)

    def main_menu(self):
        self.lcd.clear()
        self.options = ['Observation', "Photography"]
        index = 0
        self.lcd.message("{0}: {1}".format(index, self.options[index]))
        while True:
            for button in self.buttons:
                if self.lcd.is_pressed(button[0]):
                    self.lcd.clear()
                    if button[1] == 0: # You've Pressed Select
                        self.modes[self.options[index]]()
                    elif index == len(self.options) - 1 and button[1] == 1:
                        index = 0
                    elif index == 0 and button[1] == -1:
                        index = len(self.options) - 1
                    else:
                        index += button[1]
                    self.lcd.message("{0}: {1}".format(index, self.options[index]))
                    time.sleep(0.25)


    def observation_mode(self):
        self.lcd.clear()
        self.options = list(planets.keys())
        index = 0
        self.options.append("Main Menu")
        self.lcd.message("{0}: {1}".format(index, self.options[index]))
        while True:
            for button in self.buttons:
                if self.lcd.is_pressed(button[0]):
                    self.lcd.clear()
                    if button[1] == 0: # Pressed select
                        pass #TODO - begin tracking selection
                    elif button[1] == "Back": #pressed left
                        time.sleep(0.5) # Needed since buttons stay "pressed"
                        self.main_menu()
                    elif index == len(self.options) - 1 and button[1] == 1:
                        index = 0
                    elif index == 0 and button[1] == -1:
                        index = len(self.options) - 1
                    else:
                        index += button[1]
                    self.lcd.message("{0}: {1}".format(index, self.options[index]))
                    time.sleep(0.25)


    def photo_mode(self):
        self.lcd.message("Entered Photo Mode!")
        time.sleep(3)
        self.main_menu()

    def display_message(self, message:str):
        self.lcd.message(message)


if __name__ == '__main__':
    disp = Display()
    disp.main_menu()
