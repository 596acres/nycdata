from django import forms
from django.contrib import admin

from .models import Landmark


class LandmarkAdmin(admin.ModelAdmin):
    list_display = ('name', 'bbl', 'lm_type',)
    list_filter = ('lm_type',)
    search_fields = ('name', 'bbl',)
    readonly_fields = ('parcel',)


admin.site.register(Landmark, LandmarkAdmin)
