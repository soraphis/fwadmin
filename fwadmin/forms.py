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
    # reorder or something
    stock_port = forms.ModelChoiceField(queryset=SamplePort.objects.all(),
                                        required=False)
    
    def clean(self):
        cleaned_data = super(NewRuleForm, self).clean()
        port = cleaned_data.get("port")
        stock_port = cleaned_data.get("stock_port")
        print port, stock_port
        if not (port or stock_port):
            raise forms.ValidationError("Need a port number or a stock port")
        if port and stock_port:
            raise forms.ValidationError("You can not add both port and stock port")
        return cleaned_data

    class Meta:
        model = ComplexRule
        exclude = ('host', 
                   # hide for simplicity for now
                   'from_net')
