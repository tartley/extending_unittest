'''
A testrunner that augments Django's default one by highlighting test output
using colored text.

See also tests.utils.testrunner, which uses this.
'''

from functools import wraps
import time
import signal
from unittest import TextTestResult
from unittest.signals import registerResult

from django.test.simple import DjangoTestRunner
from termcolor import colored


class ColoredStream(object):
    '''
    Wraps the color assigned in '__init__' around all text passed to 'write'
    '''

    def __init__(self, wrapped, color):
        '''
        Takes a stream (like sys.stdout) and a color (a string name of a color
        as defined by termcolor, e.g. 'red')
        '''
        self.wrapped = wrapped
        self.color = color

    def write(self, text):
        self.wrapped.write(colored(text, self.color))

    def writeln(self, text):
        self.wrapped.writeln(colored(text, self.color))

    def flush(self):
        self.wrapped.flush()


def color(clr):
    '''
    Returns a decorator which patches out self.stream with a wrapper which
    colors the text written to it.
    '''

    def decorator(func):

        @wraps(func)
        def inner(self, *args):
            orig = self.stream
            self.stream = ColoredStream(self.stream, clr)
            try:
                retval = func(self, *args)
            finally:
                self.stream = orig
            return retval

        return inner

    return decorator


class ColoredTextTestResult(TextTestResult):
    '''
    Highlights important test results in color
    '''

    @color('magenta')
    def addError(self, test, err):
        TextTestResult.addError(self, test, err)

    @color('red')
    def addFailure(self, test, err):
        TextTestResult.addFailure(self, test, err)

    @color('yellow')
    def addSkip(self, test, reason):
        TextTestResult.addSkip(self, test, reason)

    @color('cyan')
    def addExpectedFailure(self, test, err):
        TextTestResult.addExpectedFailure(self, test, err)

    @color('cyan')
    def addUnexpectedSuccess(self, test):
        TextTestResult.addUnexpectedSuccess(self, test)


class ColoredTextTestRunner(DjangoTestRunner):
    '''
    Prints the final test summary using color highlighting.

    The methods in here are cut-and-paste from the base classes, then tweaked
    to produce colored output. I couldn't find a nicer way to do it.
    '''

    def run(self, *args, **kwargs):
        '''
        Runs the test suite after registering a custom signal handler
        that triggers a graceful exit when Ctrl-C is pressed.
        '''
        self._default_keyboard_interrupt_handler = signal.signal(signal.SIGINT,
            self._keyboard_interrupt_handler)
        try:
            result = self.run_inner(*args, **kwargs)
        finally:
            signal.signal(signal.SIGINT, self._default_keyboard_interrupt_handler)
        return result


    def run_inner(self, test):
        "Run the given test case or test suite."
        result = self._makeResult()
        registerResult(result)
        result.failfast = self.failfast
        result.buffer = self.buffer
        startTime = time.time()
        startTestRun = getattr(result, 'startTestRun', None)
        if startTestRun is not None:
            startTestRun()
        try:
            test(result)
        finally:
            stopTestRun = getattr(result, 'stopTestRun', None)
            if stopTestRun is not None:
                stopTestRun()
        stopTime = time.time()
        timeTaken = stopTime - startTime
        result.printErrors()
        if hasattr(result, 'separator2'):
            self.stream.writeln(result.separator2)
        run = result.testsRun
        self.stream.writeln("Ran %d test%s in %.3fs" %
                            (run, run != 1 and "s" or "", timeTaken))
        self.stream.writeln()

        expectedFails = unexpectedSuccesses = skipped = 0
        try:
            results = map(len, (result.expectedFailures,
                                result.unexpectedSuccesses,
                                result.skipped))
        except AttributeError:
            pass
        else:
            expectedFails, unexpectedSuccesses, skipped = results

        infos = []
        if result.wasSuccessful():
            self.stream.write(colored("OK", 'green', attrs=['bold']))
        else:
            self.stream.write(colored("FAILED", 'red', attrs=['bold']))
            failed, errored = map(len, (result.failures, result.errors))
            if failed:
                infos.append(colored("failures=%d" % failed, 'red'))
            if errored:
                infos.append(colored("errors=%d" % errored, 'magenta'))

        if skipped:
            infos.append(colored(
                "skipped=%d" % skipped,
                'yellow'))
        if expectedFails:
            infos.append(colored(
                "expected failures=%d" % expectedFails,
                'cyan'))
        if unexpectedSuccesses:
            infos.append(colored(
                "unexpected successes=%d" % unexpectedSuccesses,
                'cyan'))

        if infos:
            self.stream.writeln(" (%s)" % (", ".join(infos),))
        else:
            self.stream.write("\n")
        return result

