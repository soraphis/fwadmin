from django.contrib import admin
from fwadmin.models import (
    Host,
    Port,
)

admin.site.register(Host)
admin.site.register(Port)

