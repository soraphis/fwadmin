from django.test import TestCase


class IntegrationTestCase(TestCase):

    def test_pages_need_login(self):
        for view in ["new", "list"]:
            resp = self.client.get("/fwadmin/%s/" % view)
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(
                resp["Location"],
                "http://testserver/accounts/login/?next=/fwadmin/%s/" % view)

    def test_page_login(self):
        # XXX: disable LDAP auth for the tests
        #self.assertEqual(self.client.login(username="test", password="test"), True)
        pass
