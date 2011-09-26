'''
Test runner used to run the project's tests when you call "manage.py test".

See the Django docs about creating custom test runners:

https://docs.djangoproject.com/en/dev/topics/testing/#defining-a-test-runner
https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEST_RUNNER

This runner parses the environment variable TEST_RUNNER_OPTIONS to decide what
extra functionality to mix in on top of Django's test runner:


1) ALL DIRECTORIES

This finds subclasses of unittest.TestCase no matter where they are located in
the project, even in directories which are not django apps. (the default test
runner only looks in particular modules within each django app.)

This modifies the interpretation of the 'pattern' parameter passed to:

    ./manage.py test [<pattern>]

If <pattern> is omitted, then we run all tests (including the tests of all
django built-in apps and middleware), just like the default test runner.

If <pattern> is included, then we search the directory tree looking for
subclasses of unittest.TestCase. We enumerate all their methods, and construct
a testname, of the form:

    package.subpackage.module.ClassName.method_name

If <pattern> is a substring of this testname, then that test method is added to
the suite of tests to be run.

This modification to the test runner is always turned on.


2) FILTER NOISY STDOUT DURING TEST DATABASE SETUP

Django outputs lots of text while setting up the test database. This can
make it easy to miss any error messages.

This works by filtering stdout for text which matches regular expressions,
designed to match particular Django messages. Any other text which doesn't
match the regex will be passed through to stdout as usual.

Enable this filter by adding '--quiet=X' to the environment variable
TEST_RUNNER_OPTIONS, where X is: 

    0: no filtering at all
    1: suppress 'doing nothing' messages, eg. "No custom SQL for..."
    2: suppress 'trying something' messages, eg. "Checking * for fixtures..."
    3: suppress 'doing something' messages, eg. "Creating table..."
    4: suppress infrequent messages, eg. "Creating test database..."

Alternatively, '--quiet' without specifying X defaults to 3.


3) READABLE TEST NAMES

When tests are run with 'verbosity=2', this runner changes the format of test
name printing, to look like:

    package.module
        Class
            test_method1
            test_method2

This makes it easier to read by eliminating duplication. Despite the extra
lines used for modules and classes, the amount of output is actually reduced
overall due to the decreased line-wrapping.

Enable by adding '--readable' to TEST_RUNNER_OPTIONS.


4) COLOR HIGHLIGHTING OF TEST OUTPUT

Makes it easy to see at a glance if any tests have been skipped or failed
during the current test run. Is especially useful if tests are being run
with 'verbosity=2'

Enable with '--color' or '--colour' in TEST_RUNNER_OPTIONS.


5) SHOW SKIPPED TEST REPORT

At the end of the test run, this prints which tests were skipped and why.

Enable with '--show-skip' in TEST_RUNNER_OPTIONS.


5) CODE COVERAGE

Writes code coverage statistics to .coverage in order for them to be extracted
via Ned Batchelder's code coverage python tools.  Type "coverage report" or
"coverage html" in order to generate a code coverage report.

Enable by adding "--coverage"" to TEST_RUNNER_OPTIONS.

'''

import os
import sys
from unittest import TextTestResult

from django.test.simple import DjangoTestRunner
from django_jenkins.runner import CITestSuiteRunner

from .all_dirs_runner import AllDirsTestRunner
from .code_coverage import CodeCoverageMeasuringTestRunner
from .colored_runner import ColoredTextTestResult, ColoredTextTestRunner
from .filtered_runner import FilteredTestRunner
from .human_readable_result import HumanReadableTextTestResult
from .show_skipped_result import ShowSkippedResult


ENV_VAR = 'TEST_RUNNER_OPTIONS'


# Django uses three classes to run tests. The following three classes
# inherit from them and are empty except for references to each other.
# They could be used as-is to run tests exactly as Django does.

# However, further down this module, we will be augmenting these classes
# dynamically, by mixing in the class-level attributes from other testrunner
# and testresult subclasses.

class ComposedTestResult(TextTestResult):
    pass

class ComposedTestRunner(DjangoTestRunner):
    resultclass = ComposedTestResult

class TestRunner(CITestSuiteRunner):

    def __init__(self, *args, **kwargs):
        if "verbosity" in kwargs and kwargs["verbosity"] >= 2:
            print "Using " + type(self).__module__ + '.' + type(self).__name__
        super(TestRunner, self).__init__('.', *args, **kwargs)

    def run_suite(self, suite):
        runner = ComposedTestRunner(
            verbosity=self.verbosity, failfast=self.failfast,
        )
        return runner.run(suite)


class Options(object):
    '''
    Parses the TEST_RUNNER_OPTIONS env var to set boolean flags
    '''
    def __init__(self, options_str):
        self.all_dirs = True
        self.code_coverage = False
        self.color = False
        self.quiet = False
        self.readable = False
        self.show_skip = False

        if options_str:
            self.parse(options_str)


    def parse(self, options_str):
        options = options_str.split()
        for word in options:
            if word.startswith('--quiet'):
                self.quiet = True
            elif word in ["--code_coverage", "--code-coverage", "--coverage"]:
                self.code_coverage = True
            elif word == '--readable':
                self.readable = True
            elif word in ['--color', '--colour']:
                self.color = True
            elif word in ['--show_skip', '--show-skip']:
                self.show_skip = True
            else:
                sys.exit(
                    'bad entry in %s: %s.'
                    '(expect --quiet=X, --readable, --color or --show-skip)'
                    % (ENV_VAR, word)
                )


def update_class(klass, update):
    '''Copies all class-level attributes from 'update' onto 'klass'.'''
    for attr, value in vars(update).items():
        if not attr.startswith('__'):
            setattr(klass, attr, value)


def main():
    '''
    Uses the boolean attributes from Options to decide which mixins to merge
    into our test runner and test result classes.
    '''
    options = Options(os.environ.get(ENV_VAR, None))

    if options.all_dirs:
        update_class(TestRunner, AllDirsTestRunner)

    if options.color:
        update_class(ComposedTestRunner, ColoredTextTestRunner)
        update_class(ComposedTestResult, ColoredTextTestResult)

    if options.readable:
        update_class(ComposedTestResult, HumanReadableTextTestResult)

    if options.quiet:
        update_class(TestRunner, FilteredTestRunner)

    if options.show_skip:
        update_class(ComposedTestResult, ShowSkippedResult)

    if options.code_coverage:
        update_class(TestRunner, CodeCoverageMeasuringTestRunner)


main()

