
from unittest import TextTestResult


class HumanReadableTextTestResult(TextTestResult):

    def getDescription(self, test):
        '''
        Display test names using the fully qualified method
        name, not the docstring.
        '''
        return  test._testMethodName + '\n' + '.'.join([
            test.__class__.__module__,
            test.__class__.__name__,
        ])

