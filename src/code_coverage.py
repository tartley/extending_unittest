""" A test runner/result which alters Djangos test runner by making it
record code coverage information

See also test.utils.testrunner which uses this

"""

from coverage import coverage
from django.test.simple import DjangoTestSuiteRunner

filepath_regexes_to_exclude = [
    r"[A-z_\.]*test[A-z_\.]*", # tests
    r"[0-9]{4}[A-z_\.]*", # south migrations
    ]

class CodeCoverageMeasuringTestRunner(DjangoTestSuiteRunner):
    def run_tests(self, *args, **kwargs):
        """Runs the test suite, but write code coverage information to
        '.coverage' for reuse with the python coverage package."""
        cov = coverage(omit=filepath_regexes_to_exclude)
        cov.erase()
        cov.start()
        result = DjangoTestSuiteRunner.run_tests(self, *args, **kwargs)
        cov.stop()
        cov.save()
        return result
