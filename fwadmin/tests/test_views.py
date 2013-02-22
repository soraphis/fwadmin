import datetime
from urlparse import urlsplit

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import (
    User,
    Group,
)
from fwadmin.models import Host

from django_project.settings import (
    FWADMIN_ALLOWED_USER_GROUP,
    FWADMIN_DEFAULT_ACTIVE_DAYS,
)


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
            

class LoggedInViewsTestCase(TestCase):

    def setUp(self):
        allowed_group = Group.objects.get(name=FWADMIN_ALLOWED_USER_GROUP)
        self.user = User.objects.create_user("meep", password="lala")
        self.user.groups.add(allowed_group)
        res = self.client.login(username="meep", password="lala")
        self.assertTrue(res)
        self.host = Host.objects.create(
            name="host", ip="192.168.0.2", active_until="2022-01-01",
            owner=self.user)
        self.host.save()

    def test_delete_host_needs_post(self):
        resp = self.client.get(reverse("fwadmin:delete_host", 
                                       args=(self.host.id,)))
        self.assertEqual(resp.status_code, 400)

    def test_delete_host(self):
        resp = self.client.post(reverse("fwadmin:delete_host", 
                                        args=(self.host.id,)))
        self.assertEqual(resp.status_code, 302)
        with self.assertRaises(Host.DoesNotExist):
            Host.objects.get(pk=self.host.id)        

    def test_new_host(self):
        post_data = {"name": "newhost",
                     "ip": "192.168.1.1",
                    }
        resp = self.client.post(reverse("fwadmin:new_host"), post_data)
        # check the data
        host = Host.objects.get(name=post_data["name"])
        self.assertEqual(host.ip, post_data["ip"])
        self.assertEqual(host.owner, self.user)
        self.assertEqual(host.approved, False)
        self.assertEqual(host.active_until,
                         (datetime.date.today()+
                          datetime.timedelta(days=FWADMIN_DEFAULT_ACTIVE_DAYS)))
        # ensure the redirect to index works works
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(
            urlsplit(resp["Location"])[2], reverse("fwadmin:index"))
        
