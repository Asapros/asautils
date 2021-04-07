"""
This modules are extensions of python built-in types.

Examples:
    List(["a", "a", "a", "a"]).are_all_equal()
    >> True
    
    Str("Hello world").randomcase()
    >> HeLlO wOrlD
    
    Int(15).is_even()
    >> False
"""

from random   import choice as random_choice
from colorama import Fore   as fore_colorama
from colorama import init   as init_colorama
from base64   import urlsafe_b64encode
from copy     import deepcopy

class Object(object):
    def copy(self):
        """Returns deepcopy of self"""
        return deepcopy(self)
    def assign_attr(self, func):
        """Decorator to assign function or inner class to the object.
Remember that the function will be static so don't put self as an argument
Example::
    obj = EXobj()

    @obj.assign_attr
    def my_func():
        print("Hello world")

    obj.my_func()
    >>> Hello world
"""
        setattr(self, func.__name__, func)
        return func

class List(Object, list):
    def __str__(self):
        """Returns ", ".join(self)"""
        return ", ".join(self)
    def items_by_attributes(self, attributedict: dict, limit=None):
        """Searching for items that matchs all requirments
Example: get_items_by_attributes({"x":1, "y":2})
returns all objects with x=1 and y=2
"""
        itemlist = []
        for item in self:
            results = []
            for attribute in list(attributedict):
                if hasattr(item, attribute) and getattr(item, attribute) == attributedict[attribute]:
                    results.append(True)
                else:
                    results.append(False)
            if limit != None and len(itemlist) >= limit:
                    break
            if all(results):
                itemlist.append(item)
        return itemlist

    def all_equal_to(self, value) -> bool:
        """Returns false if at least 1 element is not equal to value"""
        if len(self) <= 0:
            return False
        for item in self:
            if item != value:
                return False
        return True
    def all_equal(self) -> bool:
        """Returns true if at all elements are equal"""
        if len(self) <= 0:
            return False
        else:
            value = self[0]
        for item in self:
            if item != value:
                return False
        return True
    def all_different_from(self, value) -> bool:
        """Returns false if at least 1 element is equal to value"""
        if len(self) <= 0:
            return True
        for item in self:
            if item == value:
                return False
        return True
    def all_different(self) -> bool:
        """Returns true if all elements are different"""
        if len(self) <= 0:
            return True
        to_set = set(self)
        return len(to_set) == len(self)
    def reversed(self):
        return list(reversed(self))

class Str(Object, str):
    def alphabet_ords(self) -> list:
        """Returns list of char ords in alphabet (a=0)"""
        numbers = []
        for char in self:
            if ord(char.upper()) > 64 and ord(char.upper()) < 91:
                numbers.append(ord(char.upper())-65)
            else:
                numbers.append(None)
        return numbers
    def base25_value(self) -> int:
        """Returns base25 value of string (a=0)"""
        total = 0
        alphabetvalues = self.alphabet_ords()
        alphabetvalues.reverse()
        for index in range(len(alphabetvalues)):
            if alphabetvalues[index] != None:
                total += alphabetvalues[index]*(25**index)
        return total
    def randomcase(self) -> str:
        """rETUrnS CooL StRINg FoR cOol dUdes"""
        randomstr = ""
        for char in self:
            if random_choice([True, False]):
                randomstr += char.upper()
            else:
                randomstr += char.lower()
        return randomstr
    def reverse(self) -> str:
        """Returns reversed value"""
        return self[::-1]
    def add_every_line(self, start: str="", end: str="") -> str:
        """Adds string from 'start' argument at start and 'end' at end of every line"""
        lines = self.split("\n")
        string = ""
        for line in lines:
            string += start + line + end + "\n" 
        return string[:-1]
    def nlstrip(self):
        """Something like strip, but from newlines"""
        def strip(string):
            for char in string:
                if char == "\n": string = string[1:]
                else: break
            return string
        return strip(strip(self)[::-1])[::-1]
        
    def format_colors(self):
        """
Formating string with colors. Tags:
    {red}     -> start red     color
    {green}   -> start green   color
    {blue}    -> start blue    color
    {cyan}    -> start cyan    color
    {magenta} -> start magenta color
    {yellow}  -> start yellow  color
    #------------------------------#
    {reset} -> end all colors

:param  str string: -> String to format
:return str: -> Returns colored string
        """
        init_colorama()
        return self.format(green=fore_colorama.GREEN, reset=fore_colorama.RESET, red=fore_colorama.RED, blue=fore_colorama.BLUE, cyan=fore_colorama.CYAN, yellow=fore_colorama.YELLOW, magenta=fore_colorama.MAGENTA)
    
class Int(Object, int):
    def alphabet_char(self) -> str:
        """Returns char thats in alphabet at ord of value 'self' (a=0)"""
        if self < 0 or self > 25:
            return None
        else:
            return chr(self+65)
    def reverse(self) -> int:
        """Returns reversed (as str) int"""
        return int(EXstr(self).reverse())
    def flip(self) -> int:
        """Returns flipped value (Fraction calculated by 1/self). Can handle 0"""
        try:
            return 1/self
        except ZeroDivisionError:
            return 0
    def is_even(self) -> bool:
        """Returns True if number is even"""
        return not self % 2
    def is_zero(self) -> bool:
        return not self
    def is_power2(self) -> bool:
        """Returns True if number is a power of 2
negative numbers not supported yet
"""
        number = 2
        while number <= self:
            if self == number or self == 1:
                return True
            number = number**2
        return False

class Dict(Object, dict):
    @property
    def keys(self):
        """'Fixed' version of dict.keys (It's a property, not a method)"""
        return list(super().keys())
    @property
    def values(self):
        """'Fixed' version of dict.values (It's a property, not a method)"""
        return list(super().values())
