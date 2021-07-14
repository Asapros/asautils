"""
Makes your console logs look a little bit more prettier
See more help in Logger class
"""
from datetime import datetime
from asautils.extypes import Str
from enum import Enum
from colorama import init as init_colorama
from sys import stdout

class LogTypes(Enum):
    INFO = 0
    ERROR = 1
    SUCCESS = 2
    WARNING = 3
    DEBUG = 4

TYPES_COLOR = {
    LogTypes.INFO: Str.format_colors("{blue}INFO{reset}"),
    LogTypes.ERROR: Str.format_colors("{red}ERROR{reset}"),
    LogTypes.SUCCESS: Str.format_colors("{green}SUCCESS{reset}"),
    LogTypes.WARNING: Str.format_colors("{yellow}WARNING{reset}"),
    LogTypes.DEBUG: Str.format_colors("{magenta}DEBUG{reset}")
    }

TYPES_NO_COLOR = {
    LogTypes.INFO: "INFO",
    LogTypes.ERROR: "ERROR",
    LogTypes.SUCCESS: "SUCCESS",
    LogTypes.WARNING: "WARNING",
    LogTypes.DEBUG: "DEBUG"
    }

class Logger:
    def __init__(self, name = "???", colors = True, format = "[{logtype}] -> {message}"):
        if colors:
            init_colorama()
        self.type_style = TYPES_COLOR if colors else TYPES_NO_COLOR
        self.format = format
        self.name = name

    def get_text(self, logtype, message: str) -> str:
        logtype_string = self.type_style.get(logtype, str(logtype))
        now = datetime.now()
        formatdict = {
            "logtype":logtype_string,
            "message":message,
            "name":self.name,
            "date":f"{now.strftime('%d/%m/%Y')}",
            "time":f"{now.strftime('%H:%M:%S')}",
            "timestamp":f"{datetime.timestamp(now)}"
            }
        return self.format.format(**formatdict)

    def error(self, message):
        print(self.get_text(LogTypes.ERROR, message))

    def warning(self, message):
        print(self.get_text(LogTypes.WARNING, message))

    def info(self, message):
        print(self.get_text(LogTypes.INFO, message))

    def success(self, message):
        print(self.get_text(LogTypes.SUCCESS, message))

    def debug(self, message):
        print(self.get_text(LogTypes.DEBUG, message))

# Run the script to see demo
if __name__ == "__main__":
    logger = Logger(colors = True, format = "[{logtype}] ({date} | {time} | {timestamp}) > {message}")
    logger.error("Your script crashed for no reason")
    logger.warning("Your cookies aren't baked enough")
    logger.success("Cookies succefully baked")
    logger.info("You've eaten a cookie")
    logger.debug("Hello World")
    input()
