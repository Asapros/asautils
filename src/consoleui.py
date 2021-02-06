"""
Some tools to make command line apps lot more user-friendly

Examples:
    OptionSelctor(["option1", "option2", "option3"], title="SELECT AN OPTION:").run()
    ->

SELECT AND OPTION:
option1 <
option2
option3

"""
from enum import Enum
from os import system
from pynput import keyboard
from time import sleep
from random import randint

class Sides(Enum):
    """Enum used for specifying sides of cursor in OptionSelector"""
    LEFT = 0 
    RIGHT = 1
    BOTH = 2
    # There will never be 'center' side cause it's too glitchy


def clear():
    """Clearing cmd screen"""
    system("cls")
def gen_text(text, x, y, anchor = Sides.LEFT):
    """Generating text in specific place cmd"""
    if anchor == Sides.LEFT:
        return "\033[{2};{1}H{0}".format(text, x, y)
    elif anchor == Sides.RIGHT:
        return "\033[{2};{1}H{0}".format(text, x-len(text)+1, y)

def tprint(text, mintime, maxtime, end="\n"):
    """Slowly printing text.
mintime and maxtime are in miliseconds
'end' argument will be printed at the very end"""
    for char in text:
        print(char, end="", flush=True)
        sleep(randint(mintime, maxtime)/1000)
    print(end, end="")

class OptionSelector:
    def __init__(self, options, selectchars = (">","<"), space=1, title="", selectside = Sides.RIGHT, footer=""):
        """OptionSelctor is used for creating cmd menus. Addicional arguments:
    title, footer - text that will appear before, and after options.
    space         - space between selected text and selectchar
    selectside    - specify what side do you want selecting arrows to be
    selectchars   - specify what chars will appear before and after selected option
    
"""
        self.options = options
        self.selected = 0
        self.space = space
        self.selectside = selectside
        self.selectchars = selectchars
        self.title = title
        self.footer = "\n" + footer
    def run(self):
        """OptionSelector can be runned infinite amount of times.
run() will block the main thread, and return index of selected option"""
        clear()
        self.keylistener = keyboard.Listener(on_press=self.__keypressed)
        self.keylistener.start()
        self.update()
        self.keylistener.join()
        clear()
        return self.selected
    def update(self):
        """This method is not private only in case if you'll want to change
options, title, footer or other while selecting is running. REMEMBER - run() will block main thread,
you'll need to run your code in other one."""
        optionadder = 1
        updatestr = ""
        if self.title != "":
            optionadder = 2
            updatestr = gen_text(self.title, 1, 1) 

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
                    selectedB = " " * self.space + " " * len(self.selectchars[0])
                elif self.selectside == Sides.LEFT:
                    selectedA = " " * self.space + " " * len(self.selectchars[1])
                elif self.selectside == Sides.BOTH:
                    selectedB = " " * self.space + " " * len(self.selectchars[1])
                    selectedA = " " * self.space + " " * len(self.selectchars[0])

            updatestr += gen_text(selectedA + self.options[option] + selectedB, 1, option+optionadder)
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
