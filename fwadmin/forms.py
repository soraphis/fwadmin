from django.forms import ModelForm

from .models import (
    ComplexRule,
    Host,
)


class NewHostForm(ModelForm):
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
    class Meta:
        model = ComplexRule
        exclude = ('host', )
