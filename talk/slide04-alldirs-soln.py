from inspect import getmembers, isclass
from os.path import join, relpath, splitext, walk
import sys
from unittest import TestCase, TestLoader, TestSuite
from django.test.simple import reorder_suite, DjangoTestSuiteRunner


class AllDirsTestRunner(DjangoTestSuiteRunner):

    def build_suite(self, test_labels, extra_tests=None, **kwargs):
        suite = TestSuite()
        loader = TestLoader()
        for fname in _get_module_names('.'):
            module = _import(_to_importable_name(fname))
            for test_case in _get_module_testcases(module):
                suite.addTests(loader.loadTestsFromTestCase(test_case))

        return reorder_suite(suite, (TestCase,))



def _get_module_names(root):
    '''
    Yield the filenames of all the Python modules in dir 'root' and its subdirs
    '''
    for subdir, dirs, fnames in walk(root):
        for fname in fnames:
            if fname.endswith('.py'):
                yield relpath(join(subdir, fname))



def _to_importable_name(fname):
    '''
    Convert the filename of a module into the module name used to import it.
    e.g. 'ordering/tests/my_test.py' -> 'ordering.tests.my_test'
    '''
    fname, _ = splitext(fname)
    modname = fname.replace('/', '.')
    if modname.endswith('.__init__'):
        modname = modname[:-9]
    return modname



def _import(modname):
    '''
    Given a module name in 'ordering.blobs' format, import and return it
    '''
    __import__(modname)
    return sys.modules[modname]



def _get_module_testcases(module):
    '''
    Yield all the given module's TestCases.
    '''
    for name, value in getmembers(module):
        if (isclass(value) and issubclass(value, TestCase)):
            yield value

