import datetime
import re
import json
from mock import patch

from urlparse import urlsplit

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import (
    Group,
    User,
)
from fwadmin.models import (
    ChangeLog,
    ComplexRule,
    Host,
    SamplePort,
)
from django_project.settings import (
    FWADMIN_ALLOWED_USER_GROUP,
    FWADMIN_MODERATORS_USER_GROUP,
    FWADMIN_DEFAULT_ACTIVE_DAYS,
)


def make_new_host_post_data():
    post_data = {"name": "newhost",
                 "ip": "192.168.1.1",
                "sla": True
    }
    return post_data


def make_new_rule_post_data():
    rule_name = "random rule name"
    post_data = {"name": rule_name,
                 "permit": False,
                 "ip_protocol": "UDP",
                 "from_net": "any",
                 "port_range": "1337",
    }
    return post_data


class AnonymousTestCase(TestCase):

    def test_index_need_login(self):
        # we do only test "fwadmin:index" here as the other ones
        # need paramters
        url = reverse("fwadmin:index")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(
            resp["Location"],
            "http://testserver/accounts/login/?next=%s" % url)

    def test_user_has_permission_to_view_index(self):
        User.objects.create_user("user_without_group", password="lala")
        res = self.client.login(username="user_without_group", password="lala")
        self.assertEqual(res, True)
        url = reverse("fwadmin:index")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 403)

    def test_gethostbyname(self):
        url = reverse("fwadmin:gethostbyname", args=("localhost",))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        # travis is a bit strange and returns ["127.0.0.1", "127.0.0.1"]
        self.assertEqual(set(json.loads(resp.content)), set(["127.0.0.1"]))

    @patch("socket.gethostbyname_ex")
    def test_gethostbyname_inet(self, mock_gethostbyname_ex):
        mock_gethostbyname_ex.return_value = (
            "www", [], ["8.8.8.8", "9.9.9.9"])
        url = reverse("fwadmin:gethostbyname",
                      args=("www.vielen_dank-peter.de",))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.content), ["8.8.8.8", "9.9.9.9"])

    def test_gethostbyname_invalid(self):
        url = reverse("fwadmin:gethostbyname", args=("dsakfjdfjsadfdsaf",))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.content), [])


class BaseLoggedInTestCase(TestCase):

    def setUp(self):
        # basic setup
        allowed_group = Group.objects.get(name=FWADMIN_ALLOWED_USER_GROUP)
        # create main user with a initial host/rule
        self.user = User.objects.create_user("meep", password="lala")
        self.user.groups.add(allowed_group)
        # add secondary user
        self.user2 = User.objects.create_user("owner2", password="lala")
        self.user2.groups.add(allowed_group)
        # and a user that is *not* in the right group
        self.non_fwadmin_user = User.objects.create_user("non-fwadmin-user")
        # login
        res = self.client.login(username=self.user.username, password="lala")
        self.assertTrue(res)
        self.loggedin_user = self.user
        # host
        self.host = Host.objects.create(
            name="ahost", description="some description",
            ip="192.168.0.2", active_until="2022-01-01",
            owner=self.user, owner2=self.user2)
        self.host.save()
        self.rule = ComplexRule.objects.create(
            host=self.host, name="http", permit=True, ip_protocol="TCP",
            port_range="80")
        # create other user with host/rule
        self.other_user = User.objects.create_user("Alice")
        self.other_host_name = "alice host"
        self.other_active_until = datetime.date(2036, 01, 01)
        self.other_host = Host.objects.create(
            name=self.other_host_name, ip="192.168.1.77",
            owner=self.other_user, active_until=self.other_active_until)
        self.other_rule = ComplexRule.objects.create(
            host=self.other_host, name="ssh", port_range="22")


class LoggedInViewsTestCase(BaseLoggedInTestCase):
    fixtures = ["initial_data"]

    def test_index_has_host(self):
        """Test that the index view has a html table with out test host"""
        resp = self.client.get(reverse("fwadmin:index"))
        needle = r'<a href="/fwadmin/host/%s/edit/">%s</a>' % (
                      self.host.id, self.host.ip)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(re.search(needle, resp.content))

    def test_new_host_get(self):
        resp = self.client.get(reverse("fwadmin:new_host"))
        self.assertEqual(resp.status_code, 200)

    def test_new_rule_get(self):
        resp = self.client.get(reverse("fwadmin:new_rule_for_host",
                                       args=(self.host.id,)))
        self.assertEqual(resp.status_code, 200)

    def test_delete_needs_post(self):
        for action in ["delete_host", "delete_rule"]:
            resp = self.client.get(reverse("fwadmin:%s" % action,
                                           args=(self.host.id,)))
            self.assertEqual(resp.status_code, 400)

    def test_delete_host(self):
        resp = self.client.post(reverse("fwadmin:delete_host",
                                        args=(self.host.id,)))
        self.assertEqual(resp.status_code, 302)
        with self.assertRaises(Host.DoesNotExist):
            Host.objects.get(pk=self.host.id)

    def test_renew_host(self):
        # create ancient host
        host = Host.objects.create(name="meep", ip="192.168.1.1",
                                   # XXX: should we disallow renew after
                                   #      some time?
                                   active_until="1789-01-01",
                                   owner=self.loggedin_user)
        # post to renew url
        resp = self.client.post(
            reverse("fwadmin:renew_host", args=(host.id,)),
            follow=True)
        # ensure we get something of the right message
        self.assertTrue("Thanks for renewing" in resp.content)
        # and that it is actually renewed
        host = Host.objects.get(name="meep")
        self.assertEqual(
            host.active_until,
            (datetime.date.today() +
             datetime.timedelta(days=FWADMIN_DEFAULT_ACTIVE_DAYS)))

    def test_new_host(self):
        post_data = make_new_host_post_data()
        resp = self.client.post(reverse("fwadmin:new_host"), post_data)
        # check the data
        host = Host.objects.get(name=post_data["name"])
        self.assertEqual(host.ip, post_data["ip"])
        self.assertEqual(host.owner, self.loggedin_user)
        self.assertEqual(host.approved, False)
        self.assertEqual(
            host.active_until,
            (datetime.date.today() +
             datetime.timedelta(days=FWADMIN_DEFAULT_ACTIVE_DAYS)))
        # ensure the redirect to index works works
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(
            urlsplit(resp["Location"])[2], reverse("fwadmin:new_rule_for_host",
                                                   args=(host.id,)))

    def test_new_host_owner_and_owner2_different(self):
        post_data = {"name": "newhost",
                     "ip": "192.168.1.1",
                     "owner2": self.loggedin_user.id,
                    }
        resp = self.client.post(reverse("fwadmin:new_host"), post_data)
        self.assertTrue(
            "Owner and Secondary Owner can not be the same" in resp.content)
        with self.assertRaises(Host.DoesNotExist):
            Host.objects.get(ip=post_data["ip"])

    def test_new_host_owner2_has_correct_group(self):
        post_data = {"name": "newhost",
                     "ip": "192.168.1.1",
                     "owner2": self.non_fwadmin_user.id,
                    }
        resp = self.client.post(reverse("fwadmin:new_host"), post_data)
        self.assertTrue(
            "Secondary Owner must be in group" in resp.content)
        with self.assertRaises(Host.DoesNotExist):
            Host.objects.get(ip=post_data["ip"])

    def test_edit_host(self):
        # create a new host
        initial_hostname = "My initial hostname"
        new_post_data = {"name": initial_hostname,
                         "ip": "192.168.1.1",
                         "sla": True,
                         }
        resp = self.client.post(reverse("fwadmin:new_host"), new_post_data)
        pk = Host.objects.get(name=initial_hostname).pk
        # now edit it and also try changing the IP
        edit_post_data = {"name": "edithost",
                         "ip": "192.168.99.99",
                         }
        # get the PK of the new host
        resp = self.client.post(reverse("fwadmin:edit_host", args=(pk,)),
                                edit_post_data)
        # and verify that:
        host = Host.objects.get(pk=pk)
        # name changed
        self.assertEqual(host.name, "edithost")
        # IP did not change (django forms give this for free, but its still
        # good to be paranoid if its just a single extra line)
        self.assertEqual(host.ip, "192.168.1.1")
        # and we redirect back
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(
            urlsplit(resp["Location"])[2], reverse("fwadmin:edit_host",
                args=(host.id,)))

    def test_same_owner_actions(self):
        host = self.other_host
        host_name = self.other_host_name
        for action in ["renew_host", "edit_host", "delete_host"]:
            resp = self.client.post(reverse("fwadmin:%s" % action,
                                            args=(host.id,)))
            # ensure we get a error status
            self.assertEqual(resp.status_code, 403)
            # check error message
            self.assertTrue("are not owner of this object" in resp.content)
            # ensure the active_until date is not modified
            host = Host.objects.get(name=host_name)
            self.assertEqual(
                self.other_host.active_until, self.other_active_until)

    def test_same_owner_delete_rules(self):
        resp = self.client.post(reverse("fwadmin:delete_rule",
                                            args=(self.other_rule.id,)))
        self.assertEqual(resp.status_code, 403)

    def test_same_owner_create_rules(self):
        resp = self.client.post(reverse("fwadmin:new_rule_for_host",
                                        args=(self.other_host.id,)),
                                make_new_rule_post_data())
        self.assertEqual(resp.status_code, 403)

    def test_moderator_needs_auth(self):
        resp = self.client.get(
            reverse("fwadmin:moderator_list_unapproved"))
        self.assertEqual(resp.status_code, 403)
        resp = self.client.get(
            reverse("fwadmin:moderator_approve_host", args=(1,)))
        self.assertEqual(resp.status_code, 403)

    def test_export_protected(self):
        resp = self.client.get(reverse("fwadmin:export", args=("cisco",)))
        self.assertEqual(resp.status_code, 403)

    def test_create_rules_verifciaton(self):
        rule_data = make_new_rule_post_data()
        rule_data["port_range"] = "xxx"
        resp = self.client.post(reverse("fwadmin:new_rule_for_host",
                                        args=(self.host.id,)),
                                rule_data)
        self.assertTrue("Port or Range must be a single port or a range."
            in resp.content)
        self.assertEqual(
            len(ComplexRule.objects.filter(host=self.host)), 1)

    def test_create_rules_verifciaton_range_with_space(self):
        rule_data = make_new_rule_post_data()
        rule_data["port_range"] = "4 - 42"
        resp = self.client.post(reverse("fwadmin:new_rule_for_host",
                                        args=(self.host.id,)),
                                rule_data)
        self.assertEqual(
            len(ComplexRule.objects.filter(port_range="4-42")), 1)
        self.assertEqual(resp.status_code, 302)

    def test_create_rules_verifciaton_end(self):
        rule_data = make_new_rule_post_data()
        rule_data["port_range"] = "1-x"
        resp = self.client.post(reverse("fwadmin:new_rule_for_host",
                                        args=(self.host.id,)),
                                rule_data)
        self.assertEqual(
            len(ComplexRule.objects.filter(host=self.host)), 1)
        self.assertTrue("End port must be a number" in resp.content)

    def test_create_rules_verifciaton_max(self):
        rule_data = make_new_rule_post_data()
        rule_data["port_range"] = "70000"
        resp = self.client.post(reverse("fwadmin:new_rule_for_host",
                                        args=(self.host.id,)),
                                rule_data)
        self.assertEqual(
            len(ComplexRule.objects.filter(host=self.host)), 1)
        self.assertTrue("Port can not be greater than 65535" in resp.content)

    def test_create_rules_verifciaton_order(self):
        rule_data = make_new_rule_post_data()
        rule_data["port_range"] = "20-10"
        resp = self.client.post(reverse("fwadmin:new_rule_for_host",
                                        args=(self.host.id,)),
                                rule_data)
        self.assertEqual(
            len(ComplexRule.objects.filter(host=self.host)), 1)
        self.assertTrue("Port order incorrect" in resp.content)

    def test_create_rules_from_stock(self):
        old_rules_len = len(ComplexRule.objects.filter(host=self.host))
        rule_data = make_new_rule_post_data()
        rule_data["stock_port"] = SamplePort.objects.all()[0].id
        # port range is a string
        rule_data["port_range"] = str(SamplePort.objects.all()[0].number)
        resp = self.client.post(reverse("fwadmin:new_rule_for_host",
                                        args=(self.host.id,)),
                                rule_data)
        self.assertEqual(old_rules_len + 1,
            len(ComplexRule.objects.filter(host=self.host)))


class ChangeLogTestCase(BaseLoggedInTestCase):

    def test_changelog_new_host(self):
        post_data = make_new_host_post_data()
        self.client.post(reverse("fwadmin:new_host"), post_data)
        # ensure we have a changelog for the host
        changelog = ChangeLog.objects.get(host_name=post_data["name"])
        self.assertEqual(changelog.host_ip, post_data["ip"])
        # with the rough correct "when"
        self.assertEqual(
            changelog.when.strftime("%Y-%m-%d %H"),
            datetime.datetime.now().strftime("%Y-%m-%d %H"))
        # and the change
        self.assertEqual(
            changelog.what,
            "New host %s (%s) created" % (post_data["name"],
                                          post_data["ip"]))


class ModeratorTestCase(BaseLoggedInTestCase):

    def setUp(self):
        super(ModeratorTestCase, self).setUp()
        moderators = Group.objects.get(name=FWADMIN_MODERATORS_USER_GROUP)
        self.user.groups.add(moderators)
        self.host.approved = False
        self.host.save()

    def test_moderator_approve(self):
        resp = self.client.post(reverse("fwadmin:moderator_approve_host",
                                        args=(self.host.id,)))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(
            urlsplit(resp["Location"])[2],
            reverse("fwadmin:moderator_list_unapproved"))
        # refresh from DB
        host = Host.objects.get(pk=self.host.id)
        self.assertEqual(host.approved, True)

    def test_moderator_list_unapproved(self):
        # check that the unapproved one is listed
        resp = self.client.post(reverse("fwadmin:moderator_list_unapproved"))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue("<td>%s</td>" % self.host.ip in resp.content)
        # simulate approve
        self.host.approved = True
        self.host.save()
        resp = self.client.post(reverse("fwadmin:moderator_list_unapproved"))
        self.assertFalse("<td>%s</td>" % self.host.ip in resp.content)

    def test_delete_rule(self):
        rule = ComplexRule.objects.create(
            host=self.host, name="ssh", permit=True, ip_protocol="TCP",
            port_range="22")
        resp = self.client.post(reverse("fwadmin:delete_rule",
                                       args=(rule.pk,)))
        # check that its gone
        with self.assertRaises(ComplexRule.DoesNotExist):
            ComplexRule.objects.get(pk=rule.pk)
        # check redirect
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(
            urlsplit(resp["Location"])[2],
            reverse("fwadmin:edit_host", args=(self.host.id,)))

    def test_new_rule_for_host(self):
        post_data = make_new_rule_post_data()
        resp = self.client.post(reverse("fwadmin:new_rule_for_host",
                                        args=(self.host.id,)),
                                post_data)
        # ensure we have the new rule
        rule = ComplexRule.objects.get(name=post_data["name"])
        for k, v in post_data.items():
            self.assertEqual(getattr(rule, k), v)
        # check redirect
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(
            urlsplit(resp["Location"])[2],
            reverse("fwadmin:edit_host", args=(self.host.id,)))

    def test_admin_export(self):
        moderators = Group.objects.get(name=FWADMIN_MODERATORS_USER_GROUP)
        self.user.groups.add(moderators)
        self.host.active = True
        self.host.approved = True
        self.host.active_until = (datetime.datetime.today() +
                                  datetime.timedelta(days=1))
        self.host.save()
        resp = self.client.get(reverse("fwadmin:export", args=("cisco",)))
        self.assertEqual(
            resp.content,
            "! fw rules for ahost (192.168.0.2) owned by meep created at %s\n"
            "access-list 120 permit TCP any host 192.168.0.2 eq 80" % (
                self.host.created_at
                ))

    def test_moderator_can_edit_other_host(self):
        resp = self.client.get(reverse("fwadmin:renew_host",
                                       args=(self.other_host.id,)))
        self.assertEqual(resp.status_code, 302)

        resp = self.client.get(reverse("fwadmin:edit_host",
                                       args=(self.other_host.id,)))
        self.assertEqual(resp.status_code, 200)

    def test_moderator_can_delete_other_host(self):
        resp = self.client.post(reverse("fwadmin:delete_host",
                                        args=(self.other_host.id,)))
        self.assertEqual(resp.status_code, 302)
        with self.assertRaises(Host.DoesNotExist):
            Host.objects.get(pk=self.other_host.id)

    def test_moderator_can_delete_other_rules(self):
        resp = self.client.post(reverse("fwadmin:delete_rule",
                                        args=(self.other_rule.id,)))
        self.assertEqual(resp.status_code, 302)
        with self.assertRaises(ComplexRule.DoesNotExist):
            ComplexRule.objects.get(pk=self.other_rule.id)

    def test_moderator_can_create_other_rules(self):
        post_data = make_new_rule_post_data()
        resp = self.client.post(reverse("fwadmin:new_rule_for_host",
                                        args=(self.other_host.id,)),
                                post_data)
        self.assertEqual(resp.status_code, 302)
        rule = ComplexRule.objects.get(name=post_data["name"])
        self.assertEqual(rule.host, self.other_host)


# note that it inherits from the LoggedInView, so all the tests for
# "owner" are run again for "owner2"
class Owner2TestCase(LoggedInViewsTestCase):

    def setUp(self):
        super(Owner2TestCase, self).setUp()
        # for the tests
        self.loggedin_user = self.user2
        # login as *owner2*
        self.client.login(
            username=self.user2.username, password="lala")
