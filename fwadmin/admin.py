from django.contrib import admin
from fwadmin.models import (
    Host,
    Port,
    Owner,
)

admin.site.register(Host)
admin.site.register(Port)
admin.site.register(Owner)
