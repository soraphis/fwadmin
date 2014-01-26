import netaddr

import django.forms as forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from django.conf import settings

from .models import (
    ComplexRule,
    Host,
    SamplePort,
)


class NewHostForm(ModelForm):

    owner_username = None

    sla = forms.BooleanField(label=_("SLA"), required=True)

    def __init__(self, *args, **kwargs):
        self.owner_username = kwargs.pop('owner_username', None)
        super(NewHostForm, self).__init__(*args, **kwargs)

    def clean_owner2(self):
        """ Custom validation for owner2 """
        # ensure owners are differernt
        data = self.cleaned_data.get("owner2")
        if data is None:
            return data
        # owner != owner2
        if self.owner_username == data:
            raise forms.ValidationError(
                _("Owner and Secondary Owner can not be the same."))
        # check correct group for owner2
        required_group = settings.FWADMIN_ALLOWED_USER_GROUP
        if not data.groups.filter(name=required_group):
            raise forms.ValidationError(
                _("Secondary Owner must be in group '%s'.") % required_group)
        return data

    class Meta:
        model = Host
        exclude = ('owner', 'approved', 'active', 'active_until',
                   'complex_rules')


class EditHostForm(ModelForm):

    class Meta:
        model = Host
        exclude = ('owner', 'approved', 'active', 'active_until',
                   'ip', 'complex_rules')


class NewRuleForm(ModelForm):

    IP_PROTOCOL_CHOICES = (
        ('TCP', 'TCP protocol'),
        ('UDP', 'UDP protocol'),
        )

    ip_protocol = forms.CharField(
        label=_("IP Protocol"),
        max_length=3,
        widget=forms.Select(choices=IP_PROTOCOL_CHOICES))

    stock_port = forms.ModelChoiceField(
        label=_("Standard Port"),
        queryset=SamplePort.objects.all(),
        required=False)

    port_range = forms.CharField(
        label=_("Port or range"),
        widget=forms.TextInput(attrs={'placeholder': _("22 or 1024-1030")}))

    def clean(self):
        """ Custom validation """
        cleaned_data = super(NewRuleForm, self).clean()

        # validate port_range
        port_range = cleaned_data.get("port_range")
        start, sep, end = port_range.partition("-")
        if not start.isdigit():
            raise forms.ValidationError(_("Port or Range must be a single port or a range."))
        if end and not end.isdigit():
            raise forms.ValidationError(_("End port must be a number"))
        if int(start) > 65535 or (end and int(end) > 65535):
            raise forms.ValidationError(
                _("Port can not be greater than 65535"))
        if end and int(start) >= int(end):
            raise forms.ValidationError(
                _("Port order incorrect"))

        stock_port = cleaned_data.get("stock_port")
        # XXX: no test for this yet
        from_net = cleaned_data.get("from_net")
        if from_net and from_net != "any":
            try:
                net = netaddr.IPNetwork(from_net)
                net  # pyflakes
            except netaddr.AddrFormatError:
                raise forms.ValidationError(_("Invalid network address"))
        if not (port_range or stock_port):
            raise forms.ValidationError(
                _("Need a port number or a stock port"))
        if (port_range and stock_port and port_range != stock_port.number):
            raise forms.ValidationError(_("You port and stock port differ"))
        return cleaned_data

    class Meta:
        fields = (
            'stock_port',
            'name',
            'permit',
            'ip_protocol',
            'port_range',
            'from_net',
            )
        model = ComplexRule
