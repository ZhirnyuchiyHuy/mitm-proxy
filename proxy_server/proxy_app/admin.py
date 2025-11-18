from django.contrib import admin
from .models import NetworkRule

@admin.register(NetworkRule)
class NetworkRuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'host', 'path_prefix', 'response_code', 'enable', 'created_at', 'updated_at',)
    list_editable = ('enable',)