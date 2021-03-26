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



def tprint(text, mintime, maxtime, end="\n"):
    """Types text.
:param str text:    -> Text you want to print
:param int mintime: -> Minimal time (mills)
:param int maxtime: -> Maximal time (mills)
:optional("\n") param str end: -> Same as end in print()
    """
    for char in text:
        print(char, end="", flush=True)
        sleep(randint(mintime, maxtime)/1000)
    print(end, end="")

def type_print(text, end="\n"):
    """Types text stopping on: . , -
:param str text: -> Text you want to print
:optional("\n") param str end: -> Same as end in print()
    """
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
    def __init__(self, options, selectchars = (">","<"), space=2, title="", selectside = Sides.RIGHT, footer="", trigger=None):
        """
OptionSelctor is used for creating cmd menus
:param (list,tuple) options: -> List of options you want user to choose from

:optional(">","<")     param tuple selectchars: -> Characters showing before and after selected option (depending on selectside)
:optional(1)           param int   space:       -> Space between option and selectchars
:optional("")          param str   title:       -> Title of the menu, added on the top
:optional(Sides.RIGHT) param Sides selectside:  -> Use Sides enum to specify where selectchars are going to be
:optional("")          param str   footer:      -> Same as title, except it's after all options
:optional(None)        param list  trigger:     -> List of methods. When option is selected a function will be triggered
        """
        if space < 1: space = 1
        
        self.trigger = False
        if trigger is not None:
            self.trigger = True
            self.trigger_list = trigger
        self.options = options
        self.selected = 0
        self.space = space
        self.selectside = selectside
        self.selectchars = selectchars
        self.title = title
        self.footer = footer
    def run(self):
        """Start the option selector. It can be runned infinite amount of times. WARNING: It's blocking the main thread
:return int: -> Index of selected option
:return object: -> Return value of triggered function
:raises IndexError: -> When trigger list is invalid (too short)
:raises Exception:  -> Most likely error in trigger function
        """
        try: curses.initscr()
        except AttributeError:
            print("You can't open it from IDE!")
            return
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        curses.wrapper(self.__key_listening)
        curses.endwin()
        if self.trigger:
            return self.trigger_list[self.selected]()
        else:
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
        screen.clear()
    def string(self):
        """To string method
:return str: -> Get how the option selector would look like right now.
        """
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
        """Do not care about this method please""" # TODO move selected_option to property
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
