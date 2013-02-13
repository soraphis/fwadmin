from django.db import models


class Owner(models.Model):
    owner = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    def __unicode__(self):
        return "%s <%s>" % (self.owner, self.email)


class Port(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField()
    def __unicode__(self):
        return "%s (%s)" % (self.name, self.number)


class Host(models.Model):
    name = models.CharField(max_length=200)
    ip = models.IPAddressField(max_length=100)
    active_until = models.DateField()
    owner = models.ForeignKey(Owner)
    open_ports = models.ManyToManyField(Port)
    def __unicode__(self):
        return "%s (%s): %s: %s" % (self.name, self.ip, self.active_until,
                                    self.open_ports)


