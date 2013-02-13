from django.db import models


class Owner(models.Model):
    owner = models.CharField(max_length=100)
    owner_mail = models.CharField(max_length=100)


class Host(models.Model):
    name = models.CharField(max_length=200)
    ip = models.IPAddressField(max_length=100)
    active_until = models.DateField()
    owner = models.ForeignKey(Owner)


class Port(models.Model):
    number = models.IntegerField()


class HostPort(models.Model):
    Host = models.ForeignKey(Host)
    Port = models.ForeignKey(Port)


