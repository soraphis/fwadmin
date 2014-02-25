from django.contrib import admin
from fwadmin.models import (
    ChangeLog,
    ComplexRule,
    Host,
    SamplePort,
    StaticRule,
    RulesExportToken,
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


class ChangeLogAdmin(admin.ModelAdmin):
    search_fields = ['host_name', 'host_ip', 'who']
    list_display = ['host_name', 'host_ip', 'who', 'what', 'when']
    ordering = ['when']

admin.site.register(Host, HostAdmin)
admin.site.register(SamplePort, SamplePortAdmin)
admin.site.register(ComplexRule, ComplexRuleAdmin)
admin.site.register(StaticRule)
admin.site.register(ChangeLog, ChangeLogAdmin)
admin.site.register(RulesExportToken)
