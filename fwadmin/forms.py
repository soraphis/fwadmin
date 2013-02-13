from django.forms import ModelForm

from .models import Host

class HostForm(ModelForm):
    class Meta:
        model = Host
