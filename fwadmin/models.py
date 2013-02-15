from django.db import models
from django.contrib.auth.models import User


# XXX: add "IP Protocol Number" somewhere into the data structure
class Port(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField()
    # TCP/UDP
    type = models.CharField(max_length=5)
    def __unicode__(self):
        return "%s (%s)" % (self.name, self.number)


class Host(models.Model):
    name = models.CharField(max_length=200)
    # can be ipv4,ipv6; not unique as it keeps a history
    ip = models.GenericIPAddressField()
    active_until = models.DateField()
    owner = models.ForeignKey(User)
    open_ports = models.ManyToManyField(Port)
    # approved by a admin
    approved = models.BooleanField(default=False)
    # no longer active
    active = models.BooleanField(default=False)
    def __unicode__(self):
        return "%s (%s): %s: %s %s" % (self.name, self.ip, self.active_until,
                                       self.owner, self.open_ports)



