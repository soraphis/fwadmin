from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


# XXX: this has no function yet, its meant as a simple
#      way of providing default "open this port" rules
# we may kill it if its not useful
class SamplePort(models.Model):
    """ Simple "open port" rule for a single host """
    name = models.CharField(
        max_length=100, help_text=_("The port name"))
    number = models.IntegerField(help_text=_("The port number"))
    # TCP/UDP or other IP protocol number
    type = models.CharField(max_length=5, help_text=_("IP Protocol type"))
    def __unicode__(self):
        return "%s %s (%s)" % (self.type, self.name, self.number)


class Host(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    # can be ipv4,ipv6; not unique as it keeps a history
    ip = models.GenericIPAddressField(unique=True)
    active_until = models.DateField()
    owner = models.ForeignKey(User)
    # approved by a admin
    approved = models.BooleanField(default=False)
    # no longer active
    active = models.BooleanField(default=True)
    def __unicode__(self):
        return "%s (%s): %s: %s %s" % (self.name, self.ip, self.active_until,
                                       self.owner, self.open_ports)


class ComplexRule(models.Model):
    """ Complex(er) allow/deny from net rule for a single host """
    host = models.ForeignKey(Host)
    name = models.CharField(max_length=100)
    # XXX: its not a from IP its really a network
    from_net =  models.GenericIPAddressField(default="any")
    # allow or deny
    permit = models.BooleanField(default=True)
    # TCP, UDP, anything
    ip_protocol = models.CharField(default="TCP", max_length=10)
    # just the integer
    port = models.IntegerField(blank=True, null=True)
    def __unicode__(self):
        return "complex rule: %s " % self.name
