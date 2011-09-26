'''
A test result which augments Dhango's default one by printing tests names
in a more human-readable format when 'verbosity=2'.

See also tests.utils.testrunner, which uses this.
'''

from unittest import TextTestResult


class HumanReadableTextTestResult(TextTestResult):

    last_module = None
    last_class = None

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


    def getDescription(self, test):
        '''
        Display test names using the fully qualified method name,
        not the docstring. Also, split the method name and the qualification
        onto separate lines
        '''
        return  test._testMethodName + '\n' + '.'.join([
            test.__class__.__module__,
            test.__class__.__name__,
        ])

