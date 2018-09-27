import threading
import time
import sys

def do_something():
    print('hello')
    s = input('Do you want to quit')
    if s == 'y':
        raise Quit


class Quit(Exception):
    pass

class Exception_Thread(threading.Thread):
    def run(self):
        self.thread_quit = False
        try:
            try:
                if self._target:
                    self._target(*self._args, **self._kwargs)
            finally:
                del self._target, self._args, self._kwargs

        except Quit:
            self.thread_quit = True

    def join(self):
        threading.Thread.join(self)
        return self.thread_quit


a = Exception_Thread(target=do_something)
a.start()
b = a.join()
print(b)
