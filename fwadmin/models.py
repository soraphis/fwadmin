from django.db import models


class Owner(models.Model):
    owner = models.CharField(max_length=100)
    owner_mail = models.CharField(max_length=100)


class Host(models.Model):
    name = models.CharField(max_length=200)
    ip = models.CharField(max_length=100)
    owner = models.ForeignKey(Owner)
    active_until = models.DateField()


class Port(models.Model):
    number = models.IntegerField()


class HostPort(models.Model):
    Host = models.ForeignKey(Host)
    Port = models.ForeignKey(Port)


