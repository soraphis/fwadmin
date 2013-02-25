from django.forms import ModelForm

from .models import (
    ComplexRule,
    Host,
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
    class Meta:
        model = ComplexRule
        exclude = ('host', 
                   # hide for simplicity for now
                   'from_net', 'permit', 'ip_protocol')
