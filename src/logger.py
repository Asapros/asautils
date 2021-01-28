"""
See more help with "logger" or "cmdLogTypes"
"""
import colorama
from datetime import datetime

colorama.init()
class cmdLogTypes:
    """Used by logger to display what kind of message is it"""
    info = colorama.Fore.BLUE + "INFO" + colorama.Fore.RESET
    starting = colorama.Fore.CYAN + "STARTING" + colorama.Fore.RESET
    error = colorama.Fore.RED + "ERROR" + colorama.Fore.RESET
    success = colorama.Fore.GREEN + "SUCCESS" + colorama.Fore.RESET
    warning = colorama.Fore.YELLOW + "WARNING" + colorama.Fore.RESET
    debug = colorama.Fore.MAGENTA + "DEBUG" + colorama.Fore.RESET

class logger:
    """
Will help you with visualizing what's happening in your code.
All the methods are static so there's no need of creating an object.
Examples:
    logger.formatting = x
    -> You can set your own format of message. Those will be replaced:
        - {logtype} -> ERROR, SUCCESS, etc. Depending on the situation
        - {message} -> Your message
        - {date} -> year-month-day format
        - {time} -> hour-minute-second (I belive that datetime can handle time zones automaticly)
        - {timestamp} -> timestamp
    -> If you're always using one format you can change 'formatting' permamently here
    
    log_print(logtype, message)
    -> Showing text in the console
    
    error(message)
    warning(message)
    info(message)
    starting(message)
    success(message)
    debug(message)
    -> I belive that i don't have to explain those
    """
    formatting = "[{logtype}] > {message}"
    @staticmethod
    def get_text(logtype, message):
        formatdict = {
            "logtype":logtype,
            "message":message,
            "date":f"{datetime.now().year}-{datetime.now().month}-{datetime.now().day}",
            "time":f"{datetime.now().hour}:{datetime.now().minute}.{datetime.now().second}",
            "timestamp":f"{datetime.timestamp(datetime.now())}"
            }
        return logger.formatting.format(**formatdict)
    @staticmethod
    def log_print(logtype, message):
        print(logger.get_text(logtype, message))
    @staticmethod
    def error(message):
        logger.log_print(cmdLogTypes.error, message)
    @staticmethod
    def warning(message):
        logger.log_print(cmdLogTypes.warning, message)
    @staticmethod
    def info(message):
        logger.log_print(cmdLogTypes.info, message)
    @staticmethod
    def starting(message):
        logger.log_print(cmdLogTypes.starting, message)
    @staticmethod
    def success(message):
        logger.log_print(cmdLogTypes.success, message)
    @staticmethod
    def debug(message):
        logger.log_print(cmdLogTypes.debug, message)

# Run the script to see demo
if __name__ == "__main__":
    logger.formatting = "[{logtype}] ({date} | {time} | {timestamp}) > {message}"
    logger.error("Your script crashed for no reason")
    logger.warning("Your cookies aren't baked enough")
    logger.success("Cookies succefully baked")
    logger.starting("Preparing oven to bake cookies")
    logger.info("You've eaten the cookie")
    logger.debug("Hello World")
    input()
