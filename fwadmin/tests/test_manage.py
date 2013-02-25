import datetime
from django.test import TestCase

from mock import patch

from fwadmin.management.commands.genrules import Command as GenrulesCommand
from fwadmin.management.commands.disableinactive import (
    Command as DisableInactiveCommand
)
from fwadmin.management.commands.warnexpire import Command as WarnExpireCommand

from fwadmin.models import (
    Host,
    ComplexRule,
)
from django.contrib.auth.models import User
from django_project.settings import FWADMIN_ACCESS_LIST_NR


def make_host(name, ip, owner, active_until=None, approved=True):
    if active_until is None:
        active_until = datetime.date.today() + datetime.timedelta(days=360)
    host = Host.objects.create(
        name=name, ip=ip, active_until=active_until, owner=owner, approved=approved)
    return host


def make_owner(username, email):
    owner = User.objects.create(username=username, email=email)
    return owner


# XXX: use native django fixtue support
class MyBaseTest(TestCase):

    def setUp(self):
        self.owner = make_owner("user1", "meep@example.com")
        self.host = make_host("test", "192.168.1.1", owner=self.owner)
        self.host.save()
    

class DisableInactiveTestCase(MyBaseTest):

    def setUp(self):
        MyBaseTest.setUp(self)
        self.cmd = DisableInactiveCommand()

    @patch("fwadmin.management.commands.disableinactive.ldap_user_exists")
    def test_no_gen_rules_expired(self, mock_f):
        mock_f.return_value = False
        self.assertEqual(self.host.active, True)
        self.assertEqual(self.host.approved, True)
        self.cmd.handle()
        # we need to "refresh" the host from the Db self.host is stale
        host_from_db = Host.objects.filter(pk=self.host.pk)[0]
        self.assertEqual(host_from_db.active, False)


class WarnExpireTestCase(MyBaseTest):
    
    def setUp(self):
        MyBaseTest.setUp(self)
        self.cmd = WarnExpireCommand()

    @patch("fwadmin.management.commands.warnexpire.send_renew_mail")
    def test_no_send_renew_mail_when_still_active(self, mock_f):
        """Ensure we do not send mails if there is enough delta"""
        today = datetime.date.today()
        delta = self.host.active_until-today
        self.assertEqual(delta, datetime.timedelta(days=360))
        self.cmd.handle()
        self.assertEqual(mock_f.mock_calls, [])

    @patch("fwadmin.management.commands.warnexpire.send_renew_mail")
    def test_send_renew_mail(self, mock_f):
        """Ensure we do send mails"""
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        self.host.active_until = tomorrow
        self.host.save()
        self.cmd.handle()
        mock_f.assert_called_with(self.host)


class ManagementCommandsTestCase(MyBaseTest):

    def setUp(self):
        MyBaseTest.setUp(self)
        self.cmd = GenrulesCommand()

    @patch("fwadmin.management.commands.genrules.Command._write_rules")
    def test_no_gen_rules_unapproved(self, mock_f):
        """Ensure we do not write rules for unapproved hosts"""
        self.host.approved = False
        self.host.save()
        self.cmd.print_firewall_rules()
        self.assertFalse(mock_f.called)
        self.assertEqual(mock_f.mock_calls, [])

    @patch("fwadmin.management.commands.genrules.Command._write_rules")
    def test_no_gen_rules_not_active(self, mock_f):
        """Ensure to not write rules for inactive hosts"""
        self.host.active = False
        self.host.save()
        self.cmd.print_firewall_rules()
        self.assertEqual(mock_f.mock_calls, [])

    @patch("fwadmin.management.commands.genrules.Command._write_rules")
    def test_no_gen_rules_active_until_over(self, mock_f):
        """Ensure we do not write rules for hosts that are expired"""
        self.host.active_until = datetime.date.today()
        self.host.save()
        self.cmd.print_firewall_rules()
        self.assertEqual(mock_f.mock_calls, [])

    @patch("fwadmin.management.commands.genrules.Command._write_rules")
    def test_gen_rules_complex(self, mock_f):
        """ Ensure complex rules are written """
        rule = ComplexRule.objects.create(
            host=self.host,
            name="complex", from_net="192.168.2.0/24", permit=False,
            ip_protocol="UDP", port=53)
        self.cmd.print_firewall_rules()
        mock_f.assert_called_with(
            ["! fw rules for %s (%s) owned by %s" % (
                    self.host.name, self.host.ip, self.owner.username),
             "access-list %s deny UDP 192.168.2.0/24 host 192.168.1.1 eq 53" % \
                 FWADMIN_ACCESS_LIST_NR,
             ])
    
