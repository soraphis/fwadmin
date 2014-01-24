
from django.utils import unittest
from fwadmin.models import (
    StaticRule,
    Host,
)


class StaticRuleTestCase(unittest.TestCase):

    def test_defaults(self):
        rule = StaticRule()

        self.assertEqual(rule.type, StaticRule.HEADER)
        self.assertEqual(rule.fw_type, StaticRule.FW_TYPE_CHOICES[0][0])
        self.assertEqual(rule.text, "")

    def test_rule(self):
        rule = StaticRule()
        rule.save()

        rule = StaticRule.objects.get(id=rule.id)
        self.assertEqual(rule.type, StaticRule.HEADER)
        self.assertEqual(rule.fw_type, StaticRule.FW_TYPE_CHOICES[0][0])
        self.assertEqual(rule.text, "")


class HostTestCase(unittest.TestCase):

    def test_host(self):
        host = Host(name="meep")
        self.assertEqual(host.name, "meep")
