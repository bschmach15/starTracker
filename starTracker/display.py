import Adafruit_CharLCD as LCD
from planets import planets
import time
from threading import Thread
from queue import Queue

class Display(Thread):

    def __init__(self, queue):
        # init the LCD
        self.lcd = LCD.Adafruit_CharLCDPlate()

        # set color to red
        self.lcd.set_color(1, 0, 0)
        self.lcd.message('Initializing...\n')
        self.lcd.create_char(1, [12,18,18,12,0,0,0,0])  # degree symbol
        self.lcd.create_char(2, [0,1,3,2,14,18,18,12])  # delta symbol
        self.modes = {"Main Menu": self.main_menu, "Observation": self.observation_mode, "Photography": self.photo_mode}
        self.options = None
        self.buttons = [[LCD.SELECT, 0], [LCD.LEFT, "Back"], [LCD.RIGHT,3],
                        [LCD.DOWN, 1], [LCD.UP, -1]]
        self.q = queue  #type: Queue
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
                        time.sleep(0.5)
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
                        time.sleep(0.5)
                        planet = self.options[index]
                        self.q.put(planet)
                        self.tracking_mode(planet)
                    elif button[1] == "Back":  # pressed left
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

    def tracking_mode(self, planet_key):
        tracked_planet = planets[planet_key]
        message = "Tracking {0}\nR:{1:0.2f}\x01 D:{2:0.2f}\x01".format(planet_key, tracked_planet.right_ascenscion,
                                                                   tracked_planet.declination)
        self.display_message(message)
        while True:
            for button in self.buttons:
                if self.lcd.is_pressed(button[0]):
                    if button[1] == "Back":  # pressed left
                        time.sleep(0.5)  # Needed since buttons stay "pressed"
                        self.observation_mode()



if __name__ == '__main__':
    q = Queue()
    disp = Display(q)
    disp.main_menu()
