import re
import sys
from django.test.simple import DjangoTestSuiteRunner


FILTERS = [
    re.compile("^Creating test database '"),
    re.compile("^Processing \S+ model$"),
    re.compile("^Creating table "),
    re.compile("^Adding permission '"),
    re.compile("^Running post-sync handlers for application"),
    re.compile("^Creating example.com Site object$"),
    re.compile("^No custom SQL for \S+ model$"),
    re.compile("^Installing index for \S+ model$"),
    re.compile("^Checking '\S+' for fixtures\.\.\.$"),
    re.compile("^Trying '\S+' for initial_data\.\S+ fixture 'initial_data'\.\.\.$"),
    re.compile("^Loading 'initial_data' fixtures\.\.\."),
    re.compile("^No \w+ fixture 'initial_data' in "),
    re.compile("^Checking absolute path for fixtures\.\.\."),
    re.compile("^Trying absolute path for \S+ fixture 'initial_data'\.\.\."),
    re.compile("^No fixtures found\."),
]


class FilteredStream(object):

    def __init__(self, wrapped):
        self.wrapped = wrapped

    def write(self, text):
        if not any(test.match(text) for test in FILTERS.items()):
            self.wrapped.write(text)
            self.wrapped.flush()


class FilteredTestRunner(DjangoTestSuiteRunner):

    def setup_databases(self, *args, **kwargs):
        '''
        Wrap sys.stdout to filter the noisy output while the base class
        implementation sets up the test database.
        '''
        orig = sys.stdout
        sys.stdout = FilteredStream(sys.stdout)
        try:
            return super(FilteredTestRunner, self)\
                .setup_databases(self, *args, **kwargs)
        finally:
            sys.stdout = orig

