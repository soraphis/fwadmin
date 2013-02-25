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

# XXX do we keep this form?
class EditHostForm(ModelForm):
    class Meta:
        model = Host
        exclude = ('owner', 'approved', 'active', 'active_until',
                   'open_ports',
                   'ip', 'complex_rules')


class NewRuleForm(ModelForm):
    class Meta:
        model = ComplexRule
        exclude = ('host', )
