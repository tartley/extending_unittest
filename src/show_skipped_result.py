'''
A test result which augments Django's standard one by printing the names and
reasons for skipped tests at the end of the test run.

See also tests.utils.testrunner which uses this.
'''

from unittest import TextTestResult

class ShowSkippedResult(TextTestResult):

    def printErrors(self):
        TextTestResult.printErrors(self)
        reasons = {}
        for test, reason in self.skipped:
            tests = reasons.get(reason, [])
            tests.append(test)
            reasons[reason] = tests

        if reasons:
            self.stream.writeln(self.separator1)

        for reason, tests in reasons.iteritems():
            self.stream.write('SKIP: ')
            self.stream.writeln('%dx %s' % (len(tests), reason))
            if self.showAll:
                for test in tests:
                    self.stream.writeln('  ' + '.'.join([
                        test.__class__.__module__.split('.')[-1],
                        test.__class__.__name__,
                        test._testMethodName
                    ]))

        if reasons:
            self.stream.writeln()

