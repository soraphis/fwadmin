from django.db import models
from django.contrib.auth.models import User


class Port(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField()
    def __unicode__(self):
        return "%s (%s)" % (self.name, self.number)


class Host(models.Model):
    name = models.CharField(max_length=200)
    ip = models.IPAddressField(max_length=100)
    active_until = models.DateField()
    owner = models.ForeignKey(User)
    open_ports = models.ManyToManyField(Port)
    def __unicode__(self):
        return "%s (%s): %s: %s" % (self.name, self.ip, self.active_until,
                                    self.open_ports)


