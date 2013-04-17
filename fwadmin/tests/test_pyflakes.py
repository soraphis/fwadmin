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
        cmd = 'find %s/.. -type f ! -path "*/components/*"'\
              ' -and -name "*.py"  | xargs pyflakes' % CURDIR
        p = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            close_fds=True, shell=True, universal_newlines=True)
        stdout, stderr = p.communicate()
        self.assertEqual(stderr, "")
        contents = stdout.splitlines()
        for line in contents:
            print(line)
        self.assertEqual(0, len(contents))


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
