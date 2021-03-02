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
from enum     import Enum
from os       import system
from time     import sleep
from random   import randint
from colorama import Fore
import curses

class Sides(Enum):
    """Enum used for specifying sides of cursor in OptionSelector"""
    LEFT = 0 
    RIGHT = 1
    BOTH = 2
    # There will never be 'center' side cause it's too glitchy

def format_colors(string): return string.format(green=Fore.GREEN, reset=Fore.RESET, red=Fore.RED, blue=Fore.BLUE, cyan=Fore.CYAN, yellow=Fore.YELLOW, magenta=Fore.MAGENTA)

def tprint(text, mintime, maxtime, end="\n"):
    """Slowly printing text.
mintime and maxtime are in miliseconds
'end' argument will be printed at the very end"""
    for char in text:
        print(char, end="", flush=True)
        sleep(randint(mintime, maxtime)/1000)
    print(end, end="")

def type_print(text, end="\n"):
    """Simulates text typed by someone"""
    for char in text:
        print(char, end="", flush=False)
        if char == ".":
            sleep(randint(10,15)/10)
        elif char == "," or char == "-":
            sleep(randint(6,10)/10)
        else:
            sleep(randint(80,150)/1000)
    print(end, end="")
class OptionSelector:
    def __init__(self, options, selectchars = (">","<"), space=1, title="", selectside = Sides.RIGHT, footer=""):
        """OptionSelctor is used for creating cmd menus. Addicional arguments:
    title, footer - text that will appear before, and after options.
    space         - space between selected text and selectchar
    selectside    - specify what side do you want selecting arrows to be
    selectchars   - specify what chars will appear before and after selected option
    
"""
        if space < 1: space = 1
        self.options = options
        self.selected = 0
        self.space = space
        self.selectside = selectside
        self.selectchars = selectchars
        self.title = title
        self.footer = footer
    def run(self):
        """OptionSelector can be runned infinite amount of times.
run() will block the main thread, and return index of selected option"""
        try: curses.initscr()
        except AttributeError:
            print("You can't open it from IDE!")
            return
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        curses.wrapper(self.__key_listening)
        curses.endwin()
        return self.selected
    def __key_listening(self, screen):
        while True:
            screen.clear()
            screen.addstr(self.string())
            key = screen.getch()
            screen.refresh()
            if key == curses.KEY_UP:
                self.selected = self.__limited(False, self.selected, len(self.options)-1)
            elif key == curses.KEY_DOWN:
                self.selected = self.__limited(True, self.selected, len(self.options)-1)
            elif key in (curses.KEY_ENTER, 10, 13):
                break
    def string(self):
        """To string method"""
        updatestr = ""
        if self.title != "":
            updatestr += self.title + "\n"
        padding = ["", ""]
        selected_padding = ["", ""]
        if self.selectside in (Sides.RIGHT, Sides.BOTH):
            padding[1] = " "*self.space
            selected_padding[1] = " "*(self.space-1) + self.selectchars[1]
        if self.selectside in (Sides.LEFT, Sides.BOTH):
            padding[0] = " "*self.space
            selected_padding[0] = " "*(self.space-1) + self.selectchars[0]
        

        def wrap(selected, option):
            if selected:
                return selected_padding[0] + option + selected_padding[1]
            else:
                return padding[0] + option + padding[1]
        
        for option in range(0,len(self.options)):
            if option == self.selected:
                updatestr += wrap(True, self.options[option]) + "\n"
            else:
                updatestr += wrap(False, self.options[option]) + "\n"
            


        updatestr += self.footer
        return updatestr
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
