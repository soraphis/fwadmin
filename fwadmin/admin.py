from django.contrib import admin
from fwadmin.models import (
    Host,
    SamplePort,
    ComplexRule,
    StaticRule,
)


class HostAdmin(admin.ModelAdmin):
    search_fields = ['name', 'description', 'owner__username']


class SamplePortAdmin(admin.ModelAdmin):
    search_fields = ['name', 'ip_protocol']


class ComplexRuleAdmin(admin.ModelAdmin):
    search_fields = ['host__name',
                     'host__owner__username',
                     'name',
                     'ip_protocol']

admin.site.register(Host, HostAdmin)
admin.site.register(SamplePort, SamplePortAdmin)
admin.site.register(ComplexRule, ComplexRuleAdmin)
admin.site.register(StaticRule)
