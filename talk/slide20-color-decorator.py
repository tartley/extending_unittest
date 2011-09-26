from functools import wraps

def in_color(color):
    '''
    Returns a decorator which patches out self.stream with a
    wrapper which colors the text written to it.
    '''
    def decorator(func):

        @wraps(func)
        def inner(self, *args):
            orig = self.stream
            self.stream = ColoredStream(self.stream, color)
            try:
                retval = func(self, *args)
            finally:
                self.stream = orig
            return retval

        return inner

    return decorator

