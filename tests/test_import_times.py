# coding=utf8

'''
Tests that import times for pymouse and pykeyboard are not unreasonably long.

This catches the slow-import-of-Quartz on Mac OS X due to pyobjc's slow
behavior when import via from ... import *.

Note that since this ultimately tests the import speed of pyobjc's Quartz
package, only the first test can ever fail; after that, Quartz will have been
imported and so subsequent from Quartz import * calls in later tests should
take negligible time, even if they would, on their own, be very slow.
'''

import contextlib
import time

from nose import SkipTest

@contextlib.contextmanager
def check_execution_time(description, max_seconds):
    start_time = time.time()
    yield
    end_time = time.time()
    execution_time = end_time - start_time
    if execution_time > max_seconds:
        raise Exception("Took too long to complete %s" % description)

def test_pymouse_import_time():
    # skip this test by default, call nosetests with --no-skip to enable
    raise SkipTest()
    with check_execution_time("importing pymouse", max_seconds=3):
        import pymouse

def test_pykeyboard_import_time():
    # skip this test by default, call nosetests with --no-skip to enable
    raise SkipTest()
    with check_execution_time("importing pykeyboard", max_seconds=3):
        import pykeyboard
