
from unittest import TextTestResult

from django.test.simple import DjangoTestRunner
from django_jenkins.runner import CITestSuiteRunner


class ComposedTestResult(TextTestResult):
    pass

class ComposedTestRunner(DjangoTestRunner):
    resultclass = ComposedTestResult

class TestRunner(CITestSuiteRunner):
    pass



def main():
    '''
    Uses the boolean attributes from Options to decide which mixins to merge
    into our test runner and test result classes.
    '''
    options = Options(sys.argv)

    if options.all_dirs:
        update_class(TestRunner, AllDirsTestRunner)

    if options.color:
        update_class(ComposedTestRunner, ColoredTextTestRunner)

    if options.readable:
        update_class(ComposedTestResult, HumanReadableTextTestResult)

    if options.quiet:
        update_class(TestRunner, FilteredTestRunner)

    if options.show_skip:
        update_class(ComposedTestResult, ShowSkippedResult)



def update_class(klass, update):
    '''
    Copies all class-level attributes from 'update'
    onto 'klass'.
    '''
    for attr, value in vars(update).items():
        if not attr.startswith('__'):
            setattr(klass, attr, value)


main()

