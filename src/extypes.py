"""
This modules are extensions of python built-in types.
All of them includes 'serialization' ( help(asautils.serialization) )
They're adding some new functions like 'visualization' of list and dict for example

Examples:
    EXlist(["a", "a", "a", "a"]).areAllEqual()
    >> True
    
    EXstr("Hello world").randomcase()
    >> HeLlO wOrlD
    
    EXint(15).isEven()
    >> False
    
    EXdict({"a":52, "d":["a", {"abc":256}]}).visualize()
    >>
     ├% [a: 52]
     ├: [d]┐
     │     ├# [0. "a"]
     │     ├& [1.]┐
     │     │      ├% [abc: 256]
     │     │     
     │    

"""


class EXlist(list):
    def getItemsByAttributes(self, attributedict: dict, limit=None):
        """Searching for items that matchs all requirments
Example: getItemsByAttributes({"x":1, "y":2})
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

    def areAllEqual(self, value=None) -> bool:
        """Returns false if at least 1 element is not equal to value
If value not defined checks if are elements are equal to themselfs
"""
        if len(self) <= 0 and value==None:
            return False
        elif value==None:
            value = self[0]
        for item in self:
            if item != value:
                return False
        return True
    def areAllNotEqual(self, value=None) -> bool:
        """Returns false if at least 1 element is equal to value
If value not defined checks if are elements are not equal to themselfs
"""
        if len(self) <= 0 and value==None:
            return False
        elif value==None:
            saw = []
            for item in self:
                if item in saw:
                    return False
                saw.append(item)
        else:
            for item in self:
                if item == value:
                    return False
        return True
    
    def visualize(self):
        """Visualizes values of the list"""
        string = ""
        for element in self:
            if type(element) == set or type(element) == tuple:
                element = list(element)
            elif type(element) == int:
                string += (" ├{} [%d. %d]\n" % (self.index(element), element)).format("%")
            elif type(element) == str:
                string += " ├# [%d. \"%s\"]\n" % (self.index(element), element)
            elif type(element) == bool:
                string += " ├$ [%d. %s]\n" % (self.index(element), str(element))
            elif type(element) == list:
                header = " ├: [%d.]┐" % self.index(element)
                string += header
                string += "\n" + EXstr(EXlist(element).visualize()).addEveryLine(" │" + " "*(len(header)-4)) + "\n"
            elif type(element) == dict:
                header = " ├& [%d.]┐" % self.index(element)
                string += header
                string += "\n" + EXstr(EXdict(element).visualize()).addEveryLine(" │" + " "*(len(header)-4)) + "\n"
            else:
                string += " ├> [%d. %s]\n" % (self.index(element), str(element))
                
        return string
class EXstr(str):
    def alphabetOrds(self) -> list:
        """Returns list of char ords in alphabet (a=0)"""
        numbers = []
        for char in self:
            if ord(char.upper()) > 64 and ord(char.upper()) < 91:
                numbers.append(ord(char.upper())-65)
            else:
                numbers.append(None)
        return numbers
    def base25Value(self) -> int:
        """Returns base25 value of string (a=0)"""
        total = 0
        alphabetvalues = self.alphabetOrds()
        alphabetvalues.reverse()
        for index in range(len(alphabetvalues)):
            if alphabetvalues[index] != None:
                total += alphabetvalues[index]*(25**index)
        return total
    def randomcase(self) -> str:
        """rETUrnS CooL StRINg FoR cOol dUdes"""
        from random import randint
        randomstr = ""
        for char in self:
            if randint(0,1):
                randomstr += char.upper()
            else:
                randomstr += char.lower()
        return randomstr
    def reverse(self) -> str:
        """Returns reversed value"""
        return self[::-1]
    def addEveryLine(self, start: str="", end: str="") -> str:
        """Adds string from 'start' argument at start and 'end' at end of every line"""
        lines = self.split("\n")
        string = ""
        for line in lines:
            string += start + line + end + "\n" 
        return string[:-1]
class EXint(int):
    def alphabetChar(self) ->str:
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
    def isEven(self) -> bool:
        """Returns True if number is even"""
        return self / 2 == float(self//2)
    def isZero(self) -> bool:
        return self == 0
    def isPowerOf2(self) -> bool:
        """Returns True if number is a power of 2
negative numbers not supported yet
"""
        number = 2
        while number <= self:
            if self == number or self == 1:
                return True
            number = number**2
        return False
class EXdict(dict):
    def visualize(self) -> str:
        """Visualizes values of dict """
        string = ""
        for value in list(self):
            if type(self[value]) == set or type(self[value]) == tuple:
                self[value] = list(self[value])
            elif type(self[value]) == int:
                string += (" ├{} [%s: %d]\n" % (value, self[value])).format("%")
            elif type(self[value]) == str:
                string += " ├# [%s: \"%s\"]\n" % (value, self[value])
            elif type(self[value]) == bool:
                string += " ├$ [%s: %s]\n" % (value, str(self[value]))
            elif type(self[value]) == list:
                header = " ├: [%s]┐" % value
                string += header
                string += "\n" + EXstr(EXlist(self[value]).visualize()).addEveryLine(" │" + " "*(len(header)-4))
            elif type(self[value]) == dict:
                header = " ├& [%s]┐" % value
                string += header
                string += "\n" + EXstr(EXlist(self[value]).visualize()).addEveryLine(" │" + " "*(len(header)-4))
            else:
                string += " ├> [%s]\n" % str(self[value])
        return string

            
                
