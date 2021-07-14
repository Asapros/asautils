"""
This module extends some of python built-in types and also adds new ones

Examples:
    List(["a", "a", "a", "a"]).are_all_equal()
    >> True
    
    Str("Hello world").randomcase()
    >> HeLlO wOrlD
    
    Int(15).is_even()
    >> False
"""

from random import choice as random_choice
from colorama import Fore as ColoramaFore
from hashlib import sha256

class Object(object): pass

class List(Object, list):
    def __str__(self) -> str:
        """Returns human-readable string, use repr() if you don't like it"""
        string = ""
        for element in self:
            string += str(element)
            if element is self[-1]: break
            if len(self) > 1 and element is self[-2]:
                string += " and "
                continue
            string += ", "
        return string
    
    def items_by_attributes(self, attributedict: dict, limit: int = None) -> list:
        """
Searching for items that matchs all requirments
Example: get_items_by_attributes({"x":1, "y":2})
returns all objects with x=1 and y=2
        """
        itemlist = []
        for item in self:
            results = []
            for attribute in list(attributedict):
                results.append(hasattr(item, attribute) and getattr(item, attribute) == attributedict[attribute])
            if limit is not None and len(itemlist) >= limit:
                break
            if all(results):
                itemlist.append(item)
        return itemlist

    def all_equal_to(self, value: object) -> bool:
        """Returns false if at least 1 element is not equal to value"""
        if len(self) <= 0:
            return False
        for item in self:
            if item != value:
                return False
        return True

    def get(self, index, default=None):
        """Get list element with default value"""
        try:
            return self[index]
        except IndexError:
            return default
    
    def all_equal(self) -> bool:
        """Returns true if at all elements are equal"""
        if len(self) <= 0:
            return False
        value = self[0]
        for item in self:
            if item != value:
                return False
        return True
    
    def all_different_from(self, value: object) -> bool:
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

    def register(self): # Coming soon
        raise NotImplemented

class Str(Object, str):
    def alphabet_ords(self) -> list:
        """Returns list of char ords in alphabet (a=0)"""
        numbers = []
        for char in self:
            if ord(char.upper()) not in range(65, 91):
                numbers.append(None)
                continue
            numbers.append(ord(char.upper())-65)
                
        return numbers

    def hash(self):
        """Returns hex sha256 of the string (utf-8 encoding)"""
        return sha256(self.encode("utf-8")).hexdigest()
    def plural(self):
        """Returns plural form of the word"""
        string = self
        if string.endswith("s"):
            string += "e"
        elif string.endswith("y"):
            string = string[:-1]+"ie"
        return string + "s"
        
    def base25_value(self) -> int:
        """Returns base25 value of string (a=0)"""
        total = 0
        alphabetvalues = self.alphabet_ords()
        alphabetvalues.reverse()
        for index in range(len(alphabetvalues)):
            if alphabetvalues[index] is not None:
                total += alphabetvalues[index]*(25**index)
        return total
    
    def randomcase(self) -> str:
        """rETUrnS CooL StRINg FoR cOol dUdes"""
        randomstr = ""
        for char in self:
            if random_choice([True, False]):
                randomstr += char.upper()
                continue
            randomstr += char.lower()
        return randomstr
    
    def reverse(self) -> str:
        """Returns reversed value"""
        return self[::-1]
    
    def add_every_line(self, start: str = "", end: str = "") -> str:
        """Adds string from 'start' argument at start and 'end' at end of every line"""
        lines = self.split("\n")
        string = ""
        for line in lines:
            string += start + line + end + "\n" 
        return string[:-1]
        
    def format_colors(self) -> str:
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
        """
        return self.format(
            green=ColoramaFore.GREEN,
            reset=ColoramaFore.RESET,
            red=ColoramaFore.RED,
            blue=ColoramaFore.BLUE,
            cyan=ColoramaFore.CYAN,
            yellow=ColoramaFore.YELLOW,
            magenta=ColoramaFore.MAGENTA
        )

class Int(Object, int):
    def alphabet_char(self):
        """Returns char thats in alphabet at ord of value 'self' (a=0)"""
        if self < 0 or self > 25:
            return None
        return chr(self+65)
        
    def flip(self) -> float:
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
        """
Returns True if number is a power of 2
negative numbers not supported yet
        """
        number = 2
        while number <= self:
            if self == number or self == 1:
                return True
            number = number**2
        return False

    def rotr(self, positions): # Coming soon
        """Rotates bits right"""
        raise NotImplementedError
    
    def rotl(self, positions): # Coming soon
        """Rotates bits left"""
        raise NotImplementedError

class Dict(Object, dict):
    @property
    def keys(self) -> list:
        """'Fixed' version of dict.keys (It's a property, not a method)"""
        return list(super().keys())
    
    @property
    def values(self) -> list:
        """'Fixed' version of dict.values (It's a property, not a method)"""
        return list(super().values())

class Vector2(Object, tuple):
    def __new__(cls, x, y):
        return tuple.__new__(cls, (x,y))
    @property
    def x(self): return self[0]
    @property
    def y(self): return self[1]
    def __add__(self, other):
        if not isinstance(other, self.__class__): raise TypeError("You can only add vector to vector!")
        return self.__class__(self[0]+other[0], self[1]+other[1])
    def __sub__(self, other):
        if not isinstance(other, self.__class__): raise TypeError("You can only subtract vector with vector!")
        return self.__class__(self[0]-other[0], self[1]-other[1])
    def __mul__(self, other):
        if not isinstance(other, self.__class__):
            return self.__class__(self[0]*other, self[1]*other)
        return self.__class__(self[0]*other[0], self[1]*other[1])
    def __neg__(self):
        return self.__class__(-self[0], -self[1])
    def __repr__(self):
        return "(x:%s, y:%s)" % (self[0], self[1])
