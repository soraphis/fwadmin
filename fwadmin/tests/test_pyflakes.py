#!/usr/bin/python3
# -*- Mode: Python; indent-tabs-mode: nil; tab-width: 4; coding: utf-8 -*-

# Partly based on a script from Review Board, MIT license; but modified to
# act as a unit test.

from __future__ import print_function

import os
import subprocess
import unittest

CURDIR = os.path.dirname(os.path.abspath(__file__))


class TestPyflakesClean(unittest.TestCase):

    def test_pyflakes_clean(self):
        # gather all py files we care about
        cmd = ["find", os.path.abspath(os.path.join(CURDIR, "..")),
               "-type", "f", 
               "!", "-path", "*/components/*",
               "-and",
               "-name", "*.py"]
        files = subprocess.check_output(cmd)
        # canary
        self.assertTrue("fwadmin/views.py" in files)
        # run them through pyflakes
        cmd = ["pyflakes"] + files.splitlines()
        try:
            subprocess.check_output(cmd).splitlines()
        except subprocess.CalledProcessError as e:
            self.fail("pyflakes failed with:\n%s"  % e.output)

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
