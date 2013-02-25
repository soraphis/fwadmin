
from django.utils import unittest
from fwadmin.models import (
    Host,
)


class HostTestCase(unittest.TestCase):

    def test_host(self):
        host = Host(name="meep")
        self.assertEqual(host.name, "meep")
