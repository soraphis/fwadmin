from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class Port(models.Model):
    name = models.CharField(
        max_length=100, help_text=_("The port name"))
    number = models.IntegerField(help_text=_("The port number"))

    # XXX: add allow_from and also rename to something like OpenPort or
    #      FwRule
    #
    # allows limiting the firewall to certain hosts
    #allow_from = models.GenericIPAddressField(default="0.0.0.0")

    # TCP/UDP or other IP protocol number
    type = models.CharField(max_length=5, help_text=_("IP Protocol type"))
    def __unicode__(self):
        return "%s %s (%s)" % (self.type, self.name, self.number)


class Host(models.Model):
    name = models.CharField(max_length=200)
    # can be ipv4,ipv6; not unique as it keeps a history
    ip = models.GenericIPAddressField(unique=True)
    active_until = models.DateField()
    owner = models.ForeignKey(User)
    open_ports = models.ManyToManyField(Port)
    # approved by a admin
    approved = models.BooleanField(default=False)
    # no longer active
    active = models.BooleanField(default=True)
    def __unicode__(self):
        return "%s (%s): %s: %s %s" % (self.name, self.ip, self.active_until,
                                       self.owner, self.open_ports)



