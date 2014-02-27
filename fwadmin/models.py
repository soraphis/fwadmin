from django.db import models
from django.contrib.auth.models import User

from django.forms.models import model_to_dict
from django.utils.translation import ugettext_lazy as _

import datetime


class ModelDiffMixin(object):
    """
    A model mixin that tracks model fields' values and provide some useful api
    to know what fields have been changed.

    Source: http://stackoverflow.com/questions/1355150/
            django-when-saving-how-can-you-check-if-a-field-has-changed
    """

    def __init__(self, *args, **kwargs):
        super(ModelDiffMixin, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        super(ModelDiffMixin, self).save(*args, **kwargs)
        self.__initial = self._dict

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in
                             self._meta.fields])


class ChangeLog(models.Model):
    """ Store all changes to the hosts in the DB """
    host_name = models.CharField(max_length=255, default="")
    host_ip = models.CharField(max_length=255, default="")
    who = models.CharField(max_length=255, default="")
    what = models.TextField()
    when = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s: %s" % (self.who, self.what)


class StaticRule(models.Model):
    """A static rule, free form either in the HEADER or FOOTER """
    HEADER = 0
    FOOTER = 1
    TYPE_CHOICES = (
        (HEADER, _("Header rule")),
        (FOOTER, _("Footer rule"))
    )

    FW_TYPE_CHOICES = (
        ("cisco", _("cisco")),
        ("ufw", _("ufw"))
    )

    type = models.IntegerField(default=HEADER, choices=TYPE_CHOICES)
    fw_type = models.CharField(default=FW_TYPE_CHOICES[0][0],
                                choices=FW_TYPE_CHOICES,
                                max_length=255)
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
    port_range = models.CharField(
        _("Port or range"), blank=False, null=False, default="", max_length=50)

    def __unicode__(self):
        return "complex rule: %s " % self.name


class Host(ModelDiffMixin, models.Model):
    """ A single host """
    created_at = models.DateTimeField(auto_now_add=True,
                                default=datetime.datetime.now())
    name = models.CharField(_("Name"), max_length=200)
    description = models.TextField(_("Description"), blank=True, null=True)
    # can be ipv4,ipv6
    ip = models.GenericIPAddressField(
        verbose_name=_("IP Address"), unique=True)
    active_until = models.DateField(_("Active until"))
    # main owner
    owner = models.ForeignKey(
        User, verbose_name=_("Owner"), related_name='host_owner')
    # secondary owner
    owner2 = models.ForeignKey(User, verbose_name=_("Secondary Owner"),
        null=True, blank=True, related_name='host_owner2')
    # approved by a admin
    approved = models.BooleanField(_("Approved"), default=False)
    # no longer active
    active = models.BooleanField(_("Active"), default=True)

    def get_rules_for_host(self):
        return ComplexRule.objects.filter(host=self)

    def __unicode__(self):
        return "%s (%s): %s: %s" % (self.name, self.ip, self.active_until,
                                    self.owner)


class ExportRulesToken(models.Model):
    """ A single token that allows exporting the rules without login """
    name = models.CharField(_("Name"), max_length=240)
    secret = models.CharField(_("Secret"), max_length=32)

    def __unicode__(self):
        return "token '%s' %s****" % (self.name, self.secret[0:3])
