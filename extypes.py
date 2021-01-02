# Package by Asapros (01.01.2021)
class EXlist(list):
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
    def save(self, file: str) -> bool:
        """Saving serialized list in a file
Returning result of operation
"""
        from pickle import dump
        try:
            dump(list(self), open(file, "wb"))
            return True
        except:
            return False
    def load(self, file: str) -> bool:
        """Loading serialized list from a file
Returning result of operation
"""
        from pickle import load
        try:
            newvalues = load(open(file, "rb"))
            self.clear()
            self.extend(newvalues)
            return True
        except:
            return False
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
    def addEveryLine(self, start: str) -> str:
        lines = self.split("\n")
        string = ""
        for line in lines:
            string += start + line + "\n"
        return string
class EXint(int):
    def alphabetChar(self) -> str:
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
class EXdict(dict):
    def visualize(self) -> str:
        """Visualizes values of dict """
        return self.__visualize(self)
    def __visualize(self, dictionary: dict):
        string = ""
        for value in list(dictionary):
            if type(dictionary[value]) == int:
                string += (" ├{} [%s: %d]\n" % (value, dictionary[value])).format("%")
            if type(dictionary[value]) == str:
                string += " ├# [%s: \"%s\"]\n" % (value, dictionary[value])
            if type(dictionary[value]) == bool:
                string += " ├$ [%s: %s]\n" % (value, str(dictionary[value]))
            if type(dictionary[value]) == list:
                header = " ├: [%s]┐" % value
                string += header
                string += "\n" + EXstr(self.__visualizeList(dictionary[value])).addEveryLine(" │" + " "*(len(header)-4))
            if type(dictionary[value]) == dict:
                header = " ├& [%s]┐" % value
                string += header
                string += "\n" + EXstr(self.__visualize(dictionary[value])).addEveryLine(" │" + " "*(len(header)-4))

        return string
    def __visualizeList(self, l: list):
        string = ""
        for element in l:
            if type(element) == int:
                string += (" ├{} [%d. %d]\n" % (l.index(element), element)).format("%")
            if type(element) == str:
                string += " ├# [%d. \"%s\"]\n" % (l.index(element), element)
            if type(element) == bool:
                string += " ├$ [%d. %s]\n" % (l.index(element), str(element))
            if type(element) == list:
                header = " ├: [%d.]┐" % l.index(element)
                string += header
                string += "\n" + EXstr(self.__visualizeList(element)).addEveryLine(" │" + " "*(len(header)-4))

        return string
            

            
                
