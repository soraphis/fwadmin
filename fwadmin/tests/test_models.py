
from django.utils import unittest
from fwadmin.models import (
    Host,
    User
)


class HostTestCase(unittest.TestCase):

    def test_host(self):
        host = Host(name="meep")
        self.assertEqual(host.name, "meep")

    def test_diff(self):
        user = User.objects.create_user("meep", password="lala")
        host = Host.objects.create(
                name="localhsot",
                ip="127.0.0.1",
                active_until="2022-01-01",
                owner=user)

        self.assertFalse(host.has_changed)
        self.assertEqual(len(host.changed_fields), 0)

        new_description = "New Description"
        host.description = new_description

        self.assertTrue(host.has_changed)
        self.assertEqual(len(host.changed_fields), 1)
        self.assertEqual(host.diff['description'][1], new_description)
        self.assertEqual(
            host.get_field_diff("description")[1],
            new_description)
