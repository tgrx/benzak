from django import forms
from django.contrib import admin
from django.db import models

from apps.about.models import Technology


@admin.register(Technology)
class TechnologyModelAdmin(admin.ModelAdmin):
    formfield_overrides = {models.TextField: {"widget": forms.TextInput}}
