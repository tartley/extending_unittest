'''
A test runner that augments Django's standard one by finding subclasses of
unittest.TestCase no matter where they are located in the project, even in
directories which are not django apps. (the default test runner only looks in
particular modules within each django app.)

See also tests.utils.testrunner, which uses this.
'''

from inspect import getmembers, isclass
import os
from os.path import join, relpath, splitext
import sys
from unittest import TestCase, TestLoader, TestSuite

from django.test.simple import reorder_suite, DjangoTestSuiteRunner
from django.test.testcases import TestCase as DjangoTestCase



SKIP_TEST_CLASSES = set([
    TestCase, DjangoTestCase,
])


def _get_module_names(root):
    '''
    Yield all the Python modules in the given root dir and its subdirs
    '''
    for subdir, dirs, fnames in os.walk(root):
        for fname in fnames:

            for directory in dirs:
                if directory.startswith('.') or directory == 'talk':
                    dirs.remove(directory)

            if fname.endswith('.py'):
                yield relpath(join(subdir, fname))


def _to_importable_name(fname):
    '''
    Convert the filename of a module into the module name used to import it.
    e.g. 'ordering/tests/my_test.py' -> 'esperanto.ordering.tests.my_test'
    '''
    fname, _ = splitext(fname)
    modname = fname.replace('/', '.')
    if modname.endswith('.__init__'):
        modname = modname[:-9]
    return modname


def _import(modname):
    '''
    Given a module name in 'ordering.blobs' format, imports and returns it
    '''
    __import__(modname)
    return sys.modules[modname]


def _get_testcases(module):
    '''
    Yield all the TestCase subclasses defined in the given module.
    '''
    for name, value in getmembers(module):
        if (
            isclass(value) and
            issubclass(value, TestCase) and
            value not in SKIP_TEST_CLASSES
        ):
            yield value



class AllDirsTestRunner(DjangoTestSuiteRunner):

    def _test_matches(self, testname, command_line):
        '''
        Returns True if the named test should be included in the suite
        '''
        return (
            not command_line or
            any(arg in testname for arg in command_line)
        )


    def build_suite(self, test_labels, extra_tests=None, **kwargs):
        '''
        Override the base class method to return a suite consisting of all
        TestCase subclasses throughought the whole project.
        '''
        if test_labels:
            suite = TestSuite()
        else:
            suite = DjangoTestSuiteRunner.build_suite(
                self, test_labels, extra_tests, **kwargs
            )
        added_test_classes = set(t.__class__ for t in suite)

        loader = TestLoader()
        for fname in _get_module_names(os.getcwd()):
            module = _import(_to_importable_name(fname))
            for test_class in _get_testcases(module):

                if test_class in added_test_classes:
                    continue

                for method_name in loader.getTestCaseNames(test_class):
                    testname = '.'.join([
                        module.__name__, test_class.__name__, method_name
                    ])
                    if self._test_matches(testname, test_labels):
                        suite.addTest(loader.loadTestsFromName(testname))
                        added_test_classes.add(test_class)

        return reorder_suite(suite, (TestCase,))

