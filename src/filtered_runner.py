'''
A testrunner that augment's Django's default one by filtering out the chatty
output produced while setting up test databases.

See also test_utils.testrunner, which uses this class.
'''

import os
import re
import sys

from django.test.simple import DjangoTestSuiteRunner


ENV_VAR = 'TEST_RUNNER_OPTIONS'


class FilteredStream(object):

    def __init__(self, wrapped):
        self.wrapped = wrapped
        self.filter_next_cr = False
        self.quiet = self.get_quiet_level()


    def get_quiet_level(self):
        if ENV_VAR not in os.environ:
            return 0

        for word in os.environ[ENV_VAR].split():
            if word == '--quiet':
                return 3
            if word.startswith('--quiet='):
                try:
                    _, value = word.split('=')
                    return int(value)
                except ValueError:
                    return 0
            return 0


    def write(self, text):
        if text == '\n':
            if not self.filter_next_cr:
                self.wrapped.write('\n')
            self.filter_next_cr = False
            return

        filtr = any(
            test.match(text) and level <= self.quiet
            for test, level in FILTERS.items()
        )
        if not filtr:
            self.wrapped.write(text)
            self.wrapped.flush()
        self.filter_next_cr = filtr and text[-1] != '\n'


FILTERS = {
    re.compile("^ $"): 4,
    re.compile("django_jenkins$"): 4,
    re.compile("admin$"): 4,
    re.compile("admindocs$"): 4,
    re.compile("auth$"): 4,
    re.compile("contenttypes$"): 4,
    re.compile("flatpages$"): 4,
    re.compile("messages$"): 4,
    re.compile("sessions$"): 4,
    re.compile("sites$"): 4,
    re.compile("catalog$"): 4,
    re.compile("databrowser$"): 4,
    re.compile("matching$"): 4,
    re.compile("messagedispatch$"): 4,
    re.compile("ordering$"): 4,
    re.compile("partners$"): 4,
    re.compile("reporting$"): 4,
    re.compile("south$"): 4,
    re.compile("^Creating test database '"): 4,
    re.compile("^Processing \S+ model$"): 2,
    re.compile("^Creating table "): 3,
    re.compile("^Adding permission '"): 2,
    re.compile("^Running post-sync handlers for application"): 2,
    re.compile("^Creating example.com Site object$"): 1,
    re.compile("^No custom SQL for \S+ model$"): 1,
    re.compile("^Installing index for \S+ model$"): 1,
    re.compile("^Checking '\S+' for fixtures\.\.\.$"): 1,
    re.compile("^Trying '\S+' for initial_data\.\S+ fixture 'initial_data'\.\.\.$"): 1,
    re.compile("^Loading 'initial_data' fixtures\.\.\."): 4,
    re.compile("^No \w+ fixture 'initial_data' in "): 1,
    re.compile("^Checking absolute path for fixtures\.\.\."): 1,
    re.compile("^Trying absolute path for \S+ fixture 'initial_data'\.\.\."): 1,
    re.compile("^No fixtures found\."): 4,
}


class FilteredTestRunner(DjangoTestSuiteRunner):

    def setup_databases(self, *args, **kwargs):
        '''
        Wrap sys.stdout to filter the noisy output while the base class
        implementation sets up the test database.
        '''
        ret = None
        orig = sys.stdout
        sys.stdout = FilteredStream(sys.stdout)
        try:
            ret = DjangoTestSuiteRunner.setup_databases(self, *args, **kwargs)
        finally:
            sys.stdout = orig
        return ret

