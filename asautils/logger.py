"""
See more help with "Logger" or "CmdLogTypes"
"""
from datetime import datetime
from asautils.extypes import EXstr


class CmdLogTypes:
    """Used by Logger to display what kind of message is it"""
    info     = EXstr("{blue}INFO{reset}"     ).format_colors()
    starting = EXstr("{cyan}STARTING{reset}" ).format_colors()
    error    = EXstr("{red}ERROR{reset}"     ).format_colors()
    success  = EXstr("{green}SUCCESS{reset}" ).format_colors()
    warning  = EXstr("{yellow}WARNING{reset}").format_colors()
    debug    = EXstr("{magenta}DEBUG{reset}" ).format_colors()

class Logger:
    """
Will help you with visualizing what's happening in your code.
All the methods are static so there's no need of creating an object.
Examples:
    Logger.formatting = x
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
        return Logger.formatting.format(**formatdict)
    @staticmethod
    def log_print(logtype, message):
        print(Logger.get_text(logtype, message))
    @staticmethod
    def error(message):
        Logger.log_print(CmdLogTypes.error, message)
    @staticmethod
    def warning(message):
        Logger.log_print(CmdLogTypes.warning, message)
    @staticmethod
    def info(message):
        Logger.log_print(CmdLogTypes.info, message)
    @staticmethod
    def starting(message):
        Logger.log_print(CmdLogTypes.starting, message)
    @staticmethod
    def success(message):
        Logger.log_print(CmdLogTypes.success, message)
    @staticmethod
    def debug(message):
        Logger.log_print(CmdLogTypes.debug, message)

# Run the script to see demo
if __name__ == "__main__":
    Logger.formatting = "[{logtype}] ({date} | {time} | {timestamp}) > {message}"
    Logger.error("Your script crashed for no reason")
    Logger.warning("Your cookies aren't baked enough")
    Logger.success("Cookies succefully baked")
    Logger.starting("Preparing oven to bake cookies")
    Logger.info("You've eaten the cookie")
    Logger.debug("Hello World")
    input()
