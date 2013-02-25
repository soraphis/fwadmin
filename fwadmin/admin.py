from django.contrib import admin
from fwadmin.models import (
    Host,
    SamplePort,
    ComplexRule,
)

admin.site.register(Host)
admin.site.register(SamplePort)
admin.site.register(ComplexRule)
