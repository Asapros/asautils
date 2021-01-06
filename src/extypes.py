from serialization import Serializable

class EXlist(list, Serializable):
    def getItemsByAttribute(self, attribute: str, value, **kwargs) -> list:
        """Returns all objects from list wich 'attribute' is equal to 'value'
Use 'limit' keyword in args as maximum lenght of found elements
"""
        itemlist = []
        limit = None
        if "limit" in kwargs: limit = kwargs["limit"]
        for item in self:
            if hasattr(item, attribute) and getattr(item, attribute) == value:
                if limit != None and len(itemlist) >= limit:
                    break
                itemlist.append(item)
        return itemlist
    def getItemsByAttributes(self, attributedict: dict, **kwargs):
        """Searching for items that matchs all requirments
Example: getItemsByAttributes({"x":1, "y":2})
returns all objects with x=1 and y=2
"""
        itemlist = []
        limit = None
        if "limit" in kwargs: limit = kwargs["limit"]
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

    def areAllEqual(self, value) -> bool:
        """Returns false if at least 1 element is not equal to value"""
        for item in self:
            if item != value:
                return False
        return True
    def areAllNotEqual(self, value) -> bool:
        """Returns false if at least 1 element is equal to value"""
        for item in self:
            if item == value:
                return False
        return True
    
    def visualize(self):
        """Visualizes values of the list"""
        string = ""
        for element in self:
            if type(element) == int:
                string += (" ├{} [%d. %d]\n" % (self.index(element), element)).format("%")
            if type(element) == str:
                string += " ├# [%d. \"%s\"]\n" % (self.index(element), element)
            if type(element) == bool:
                string += " ├$ [%d. %s]\n" % (self.index(element), str(element))
            if type(element) == list:
                header = " ├: [%d.]┐" % self.index(element)
                string += header
                string += "\n" + EXstr(EXlist(element).visualize()).addEveryLine(" │" + " "*(len(header)-4))
            if type(element) == dict:
                header = " ├& [%d.]┐" % self.index(element)
                string += header
                string += "\n" + EXstr(EXdict(element).visualize()).addEveryLine(" │" + " "*(len(header)-4))
        return string
class EXstr(str, Serializable):
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
    def addEveryLine(self, start: str) -> str:
        lines = self.split("\n")
        string = ""
        for line in lines:
            string += start + line + "\n"
        return string
class EXint(int, Serializable):
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
class EXdict(dict, Serializable):
    def visualize(self) -> str:
        """Visualizes values of dict """
        string = ""
        for value in list(self):
            if type(self[value]) == int:
                string += (" ├{} [%s: %d]\n" % (value, self[value])).format("%")
            if type(self[value]) == str:
                string += " ├# [%s: \"%s\"]\n" % (value, self[value])
            if type(self[value]) == bool:
                string += " ├$ [%s: %s]\n" % (value, str(self[value]))
            if type(self[value]) == list:
                header = " ├: [%s]┐" % value
                string += header
                string += "\n" + EXstr(EXlist(self[value]).visualize()).addEveryLine(" │" + " "*(len(header)-4))
            if type(self[value]) == dict:
                header = " ├& [%s]┐" % value
                string += header
                string += "\n" + EXstr(EXlist(self[value]).visualize()).addEveryLine(" │" + " "*(len(header)-4))
        return string

            
                
