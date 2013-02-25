import django.forms as forms
from django.forms import ModelForm

from .models import (
    ComplexRule,
    Host,
    SamplePort,
)


class NewHostForm(ModelForm):
    class Meta:
        model = Host
        exclude = ('owner', 'approved', 'active', 'active_until',
                   'open_ports',
                   'complex_rules')

class EditHostForm(ModelForm):
    class Meta:
        model = Host
        exclude = ('owner', 'approved', 'active', 'active_until',
                   'open_ports',
                   'ip', 'complex_rules')


class NewRuleForm(ModelForm):
    IP_PROTOCOL_CHOICES = (
        ('TCP', 'TCP protocol'),
        ('UDP', 'UDP protocol'),
        )
    ip_protocol = forms.CharField(
            max_length=3,
            widget=forms.Select(choices=IP_PROTOCOL_CHOICES))
    #port = forms.ModelChoiceField(queryset=SamplePort.objects.all())
    class Meta:
        model = ComplexRule
        exclude = ('host', 
                   # hide for simplicity for now
                   'from_net')
