#
from enum import Enum
from pynput import keyboard
from os import system

class Sides(Enum):
    LEFT = 0 
    RIGHT = 1
    BOTH = 2
    # There will never be 'center' side cause it's too glitchy


def clear(): system("cls")
def genText(text, x, y, anchor = Sides.LEFT):
    if anchor == Sides.LEFT:
        return "\033[{2};{1}H{0}".format(text, x, y)
    elif anchor == Sides.RIGHT:
        return "\033[{2};{1}H{0}".format(text, x-len(text)+1, y)

class OptionSelector:
    def __init__(self, options, selectchars = (">","<"), space=1, title="", selectside = Sides.RIGHT, footer=""):
        self.options = options
        self.selected = 0
        self.space = space
        self.selectside = selectside
        self.selectchars = selectchars
        self.title = title
        self.footer = "\n" + footer
    def run(self):
        clear()
        self.keylistener = keyboard.Listener(on_press=self.__keypressed)
        self.keylistener.start()
        self.update()
        self.keylistener.join()
        clear()
        return self.selected
    def update(self):
        optionadder = 1
        updatestr = ""
        if self.title != "":
            optionadder = 2
            updatestr = genText(self.title, 1, 1) 

        for option in range(0,len(self.options)):
            selectedA = ""
            selectedB = ""
            if self.selected == option:
                if self.selectside == Sides.RIGHT:
                    selectedB = " "*self.space + self.selectchars[1]
                elif self.selectside == Sides.LEFT:
                    selectedA = self.selectchars[0] + " " * self.space
                elif self.selectside == Sides.BOTH:
                    selectedB = " " * self.space + self.selectchars[1]
                    selectedA = self.selectchars[0] + " " * self.space
            else:
                if self.selectside == Sides.RIGHT:
                    selectedB = " " * self.space + " "
                elif self.selectside == Sides.LEFT:
                    selectedA = " " * self.space + " "
                elif self.selectside == Sides.BOTH:
                    selectedB = " " * self.space + " "
                    selectedA = " " * self.space + " "

            updatestr += genText(selectedA + self.options[option] + selectedB, 1, option+optionadder)
        updatestr += self.footer
        print(updatestr)
    def __keypressed(self, key):
        if "char" in dir(key):
            pass
        else:
            if key == keyboard.Key.enter:
                input()
                return False
            elif key == keyboard.Key.up:
                self.selected = self.__limited(False, self.selected, len(self.options)-1)
            elif key == keyboard.Key.down:
                self.selected = self.__limited(True, self.selected, len(self.options)-1)
            self.update()
    def __limited(self, operation, variable, limit):
        if operation:
            if variable >= limit:
                return 0
            else:
                return variable + 1
        else:
            if variable <= 0:
                return limit
            else:
                return variable - 1
