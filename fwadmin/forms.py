from django.forms import ModelForm

from .models import Host


class HostForm(ModelForm):
    class Meta:
        model = Host
        # alternatively use "editable=False" in model.py
        exclude = ('owner', 'approved', 'active_until', 'active')
        
