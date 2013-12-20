#!/usr/bin/python

import os
import subprocess

from django.utils import unittest


class I18nTestCase(unittest.TestCase):

    def test_i18n_compiles(self):
        with open(os.devnull, "w") as devnull:
            appdir = os.path.join(os.path.dirname(__file__), "..")
            cmd = ["python", "../manage.py", "compilemessages"]
            ret_code = subprocess.call(cmd, cwd=appdir, stdout=devnull)
            self.assertEqual(ret_code, 0)
