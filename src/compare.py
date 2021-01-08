"""
This module requires colorama
Exemples:
    percent(7, 28)
    >>> 25.0
    compare(7, 28)
    >>>
    Filled: (7/28) 25.0%
    | ++-------- |
    Display lenght: 10
    
"""
import colorama
def percent(num: int, outof: int) -> float:
    """Calculates percent of 2 numbers"""
    return (num/outof)*100
def compare(num1: int, num2: int, lenghtdiv: int=10) -> str:
    """Returns comparison string of 2 numbers
Use 'lenghtdiv' keyword to divide lenght of visualization string
"""
    colorama.init()
    perc = percent(num1, num2)
    left = 100 - perc
    string = ""
    string += "Filled: ({}/{}) {}%\n".format(num1, num2,perc)
    visualization = "| " + colorama.Fore.GREEN + "+"*round(perc/lenghtdiv) + colorama.Fore.RED + "-"*round(left/lenghtdiv) + colorama.Fore.RESET + " |"
    string += visualization
    string += "\nDisplay lenght: %d" % (len(visualization)-19)
    return string
