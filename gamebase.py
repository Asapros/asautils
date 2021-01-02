# Package by Asapros (01.01.2021)
class Game:
    def __init__(self, mainmethod, *args):
        """Base for mostly cmd games"""
        self.mainmethod = mainmethod
        self.nonblockings = []
        if len(args):
            self.nonblockings = args[0]
        self.running = False
        self.running_nonblockings = False
    def run(self):
        """Repeats 'self.mainmethod' until 'self.running' is false executed"""
        self.running = True
        while self.running: self.mainmethod()
    def run_nonblockings(self):
        """Repeats all methods passed as *args until 'self.running_nonblockings' is false"""
        self.running_nonblockings = True
        from threading import Thread
        thread = Thread(target=self.__nonblockings_execute)
        thread.start()
    def __nonblockings_execute(self):
        """Private method running in a thread after 'self.run_nonblockings' executed"""
        while self.running_nonblockings:
            for method in self.nonblockings:
                method()
    def stop(self):
        """Setting 'self.running' to false"""
        self.running = False
    def stop_nonblockings(self):
        """Settings 'self.running_nonblockings' to false"""
        self.running_nonblockings = False
    def kill(self):
        """Killing all game loops"""
        self.stop()
        self.stop_nonblockings()
