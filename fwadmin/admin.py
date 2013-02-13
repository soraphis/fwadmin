from django.contrib import admin
from fwadmin.models import (
    Host,
    Port,
    HostPort,
    Owner,
)

admin.site.register(Host)
admin.site.register(Port)
admin.site.register(HostPort)
admin.site.register(Owner)
