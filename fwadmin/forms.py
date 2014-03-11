import django.forms as forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from django.conf import settings

from .models import (
    ComplexRule,
    Host,
    SamplePort,
)

from .validators import (
    validate_port,
    validate_from_net)


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
        validators=[validate_port],
        widget=forms.TextInput(attrs={'placeholder': _("22 or 1024-1030")}))

    popover = {'data-container': ("body"), 'data-toggle': ("popover"),
                'data-trigger': ("focus"), 'data-placement': ("bottom"),
                'data-content': _("CIDR and netmask form possible")}

    attributes = {'class': "form-control",
                  'placeholder': _("any or 136.199.x.y/24")}
    attributes.update(popover)

    from_net = forms.CharField(
        validators=[validate_from_net],
        widget=forms.TextInput(attrs=attributes))

    def clean_port_range(self):
        return self.cleaned_data['port_range'].replace(" ", "")

    def clean(self):
        """ Custom validation """
        cleaned_data = super(NewRuleForm, self).clean()

        port_range = cleaned_data.get("port_range")
        stock_port = cleaned_data.get("stock_port")
        if not (port_range or stock_port):
            raise forms.ValidationError(
                _("Need a port number or a stock port"))
        if (port_range and
            stock_port and
            int(port_range) != stock_port.number):
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
