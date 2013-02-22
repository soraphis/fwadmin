from django.core.urlresolvers import reverse
from django.db import models
from django.test import TestCase
from django.contrib.auth.models import (
    User,
    Group,
)
from fwadmin.models import Host

from django_project.settings import FWADMIN_ALLOWED_USER_GROUP

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
        user = User.objects.create_user("user_without_group", password="lala")
        res = self.client.login(username="user_without_group", password="lala")
        self.assertEqual(res, True)
        url = reverse("fwadmin:index")
        resp = self.client.get(url)
        print resp, resp.content
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
