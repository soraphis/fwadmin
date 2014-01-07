from django.contrib import admin
from fwadmin.models import (
    ChangeLog,
    ComplexRule,
    Host,
    SamplePort,
    StaticRule,
)

admin.site.register(Host)
admin.site.register(SamplePort)
admin.site.register(ComplexRule)
admin.site.register(StaticRule)
admin.site.register(ChangeLog)
