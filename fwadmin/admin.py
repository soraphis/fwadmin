from django.contrib import admin
from fwadmin.models import (
    Host,
    Port,
    ComplexRule,
)

admin.site.register(Host)
admin.site.register(Port)
admin.site.register(ComplexRule)
