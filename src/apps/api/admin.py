from django.contrib import admin

from apps.api.models import ApiSettings


@admin.register(ApiSettings)
class ApiSettingsModelAdmin(admin.ModelAdmin):
    pass
