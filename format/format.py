import string
import inspect


class Formatter(string.Formatter):

    def __init__(self, f_locals, f_globals):
        self._locals = f_locals
        self._globals = f_globals

    def get_field(self, name, *args, **kwargs):
        return (eval(name, self._globals, self._locals), name)


def f(fmt):
    frame = inspect.currentframe()
    try:
        return Formatter(frame.f_back.f_locals, frame.f_back.f_globals).format(fmt)
    finally:
        del frame
