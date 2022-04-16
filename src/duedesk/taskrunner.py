# ------------------------------------------------------------------------------
# Project  : DueDesk
# Module   : Taskrunner
# Abstract : 
#   A `Taskrunner` stores the internal timmer for the currently running task. It
#   is a simple timer module able to be shared by reference to all tasks.
# ------------------------------------------------------------------------------
import time

class Taskrunner:
    def __init__(self, inner: bool):
        '''Creates a `Taskrunner` instance.'''
        self._start = 0
        self._inner = inner
        pass


    def is_running(self) -> bool:
        '''Checks if the timer is running.'''
        return self._inner


    def enable(self):
        '''Begins the timer.'''
        self._start = time.time()
        self._inner = True
        pass


    def disable(self) -> float:
        '''Stops the timer and returns the number of minutes elapsed.'''
        self._inner = False
        elapsed = time.time() - self._start
        # https://stackoverflow.com/questions/27779677/how-to-format-elapsed-time-from-seconds-to-hours-minutes-seconds-and-milliseco
        hours, rem = divmod(elapsed, 3600.0)
        minutes, seconds = divmod(rem, 60.0)
        return round(float(hours*60 + minutes + (seconds/60.0)), 2)
    pass