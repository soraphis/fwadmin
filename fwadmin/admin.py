from django.contrib import admin
from fwadmin.models import (
    Host,
    SamplePort,
    ComplexRule,
    StaticRule,
)

admin.site.register(Host)
admin.site.register(SamplePort)
admin.site.register(ComplexRule)
admin.site.register(StaticRule)
