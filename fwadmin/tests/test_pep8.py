import os
import subprocess
import unittest


class PackagePep8TestCase(unittest.TestCase):

    def test_all_code(self):
        res = 0
        py_dir = os.path.join(os.path.dirname(__file__), "..")
        res += subprocess.call(
            ["pep8",
             "--exclude", "tastypie_test_v0912.py",
             "--repeat", py_dir])
        self.assertEqual(res, 0)


if __name__ == "__main__":
    unittest.main()
