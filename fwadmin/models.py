from django.db import models
from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _


class StaticRule(models.Model):
    """A static rule, free form either in the HEADER or FOOTER """
    HEADER = 0
    FOOTER = 1
    TYPE_CHOICES = (
        (HEADER, _("Header rule")),
        (FOOTER, _("Footer rule"))
    )
    type = models.IntegerField(default=HEADER, choices=TYPE_CHOICES)
    text = models.TextField()


class SamplePort(models.Model):
    """ A open port for the UI """
    name = models.CharField(_("Name"),
        max_length=100, help_text=_("The port name"))
    number = models.IntegerField(_("Number"), help_text=_("The port number"))
    # TCP/UDP or other IP protocol number
    ip_protocol = models.CharField(_("IP Protocol"),
        max_length=5, help_text=_("IP Protocol type"))

    def __unicode__(self):
        return "%s %s (%s)" % (self.ip_protocol, self.name, self.number)


class ComplexRule(models.Model):
    """ Complex(er) allow/deny from net rule for a single host """
    host = models.ForeignKey('Host')
    name = models.CharField(_("Name"), max_length=100)
    # its not a from IP its really a network
    from_net = models.CharField(
        _("From network"), default="any", max_length=100)
    # allow or deny
    permit = models.BooleanField(_("Permit"), default=True)
    # TCP, UDP, anything
    ip_protocol = models.CharField(
        _("IP Protocol"), default="TCP", max_length=10)
    # just the integer
    port = models.IntegerField(_("Port"), blank=True, null=True)

    def __unicode__(self):
        return "complex rule: %s " % self.name


class Host(models.Model):
    """ A single host """
    name = models.CharField(_("Name"), max_length=200)
    description = models.TextField(_("Description"), blank=True, null=True)
    # can be ipv4,ipv6
    ip = models.GenericIPAddressField(
        verbose_name=_("IP Address"), unique=True)
    active_until = models.DateField(_("Active until"))
    owner = models.ForeignKey(User)
    # approved by a admin
    approved = models.BooleanField(_("Approved"), default=False)
    # no longer active
    active = models.BooleanField(_("Active"), default=True)

    def get_rules_for_host(self):
        return ComplexRule.objects.filter(host=self)

    def __unicode__(self):
        return "%s (%s): %s: %s" % (self.name, self.ip, self.active_until,
                                    self.owner)
