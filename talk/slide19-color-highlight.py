
from unittest import TextTestResult


class ColoredTextTestResult(TextTestResult):
    '''
    Highlights important test results in color
    '''
    @in_color('magenta')
    def addError(self, test, err):
        TextTestResult.addError(self, test, err)

    @in_color('red')
    def addFailure(self, test, err):
        TextTestResult.addFailure(self, test, err)

    @in_color('yellow')
    def addSkip(self, test, reason):
        TextTestResult.addSkip(self, test, reason)

    @in_color('cyan')
    def addExpectedFailure(self, test, err):
        TextTestResult.addExpectedFailure(self, test, err)

    @in_color('cyan')
    def addUnexpectedSuccess(self, test):
        TextTestResult.addUnexpectedSuccess(self, test)

