
from unittest import TextTestResult


class HumanReadableTextTestResult(TextTestResult):

    def __init__(self, *args, **kwargs):
        super(HumanReadableTextTestResult, self).__init__(*args, **kwargs)
        self.last_module = None
        self.last_class = None

    def human_readable_test_name(self, test):
        '''
        Return a test method's fully-qualified name as a multi-line string:
        
            package.module
                Class
                    method

        but if the module or class are the same as the last requested test,
        then they are omitted.
        '''
        retval = ''
        if test.__class__.__module__ != self.last_module:
            retval = test.__class__.__module__ + '\n'
            self.last_module = test.__class__.__module__
        if test.__class__ != self.last_class:
            retval += '   ' + test.__class__.__name__ + '\n'
            self.last_class = test.__class__
        retval += '      ' + test._testMethodName
        return retval


    def startTest(self, test):
        '''
        When starting a test, don't print it's description but instead its
        human_readable_test_name
        '''
        super(TextTestResult, self).startTest(test)
        if self.showAll:
            self.stream.write(self.human_readable_test_name(test))
            self.stream.write(" ... ")
            self.stream.flush()

